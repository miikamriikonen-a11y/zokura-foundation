#!/usr/bin/env python3
"""
Sijoittaminen tyona ja tieteena - PDF generator
Author: Kodo Zokura / Zokura Foundation 2026
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT

# Register font
pdfmetrics.registerFont(TTFont('ArialUni', '/Library/Fonts/Arial Unicode.ttf'))

OUTPUT = '/Users/miikariikonen/Desktop/YOMI/shared/research/sijoittaminen_tyo_ja_tiede.pdf'

# Colors
DARK = HexColor('#1a1a2e')
ACCENT = HexColor('#16213e')
GOLD = HexColor('#c9a227')
MEDIUM = HexColor('#333333')
LIGHT_GRAY = HexColor('#666666')
RULE_COLOR = HexColor('#cccccc')

# Styles
styles = {}

styles['title'] = ParagraphStyle(
    'Title', fontName='ArialUni', fontSize=28, leading=34,
    textColor=DARK, alignment=TA_CENTER, spaceAfter=6*mm
)
styles['subtitle'] = ParagraphStyle(
    'Subtitle', fontName='ArialUni', fontSize=14, leading=18,
    textColor=LIGHT_GRAY, alignment=TA_CENTER, spaceAfter=4*mm
)
styles['author'] = ParagraphStyle(
    'Author', fontName='ArialUni', fontSize=12, leading=16,
    textColor=ACCENT, alignment=TA_CENTER, spaceAfter=2*mm
)
styles['h1'] = ParagraphStyle(
    'H1', fontName='ArialUni', fontSize=18, leading=24,
    textColor=DARK, spaceBefore=12*mm, spaceAfter=6*mm
)
styles['h2'] = ParagraphStyle(
    'H2', fontName='ArialUni', fontSize=14, leading=18,
    textColor=ACCENT, spaceBefore=8*mm, spaceAfter=4*mm
)
styles['body'] = ParagraphStyle(
    'Body', fontName='ArialUni', fontSize=10.5, leading=15,
    textColor=MEDIUM, alignment=TA_JUSTIFY, spaceAfter=3*mm
)
styles['quote'] = ParagraphStyle(
    'Quote', fontName='ArialUni', fontSize=10, leading=14,
    textColor=LIGHT_GRAY, alignment=TA_LEFT,
    leftIndent=15*mm, rightIndent=10*mm,
    spaceBefore=4*mm, spaceAfter=4*mm
)
styles['ref'] = ParagraphStyle(
    'Ref', fontName='ArialUni', fontSize=9, leading=13,
    textColor=LIGHT_GRAY, leftIndent=10*mm, spaceBefore=1*mm, spaceAfter=1*mm
)
styles['footer_style'] = ParagraphStyle(
    'Footer', fontName='ArialUni', fontSize=8, leading=10,
    textColor=LIGHT_GRAY, alignment=TA_CENTER
)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('ArialUni', 8)
    canvas.setFillColor(LIGHT_GRAY)
    canvas.drawCentredString(A4[0]/2, 15*mm, 'Zokura Foundation 2026')
    canvas.drawRightString(A4[0] - 20*mm, 15*mm, f'{doc.page}')
    canvas.restoreState()


def cover_page(canvas, doc):
    canvas.saveState()
    # Top accent line
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(2)
    canvas.line(30*mm, A4[1] - 40*mm, A4[0] - 30*mm, A4[1] - 40*mm)
    # Bottom accent line
    canvas.line(30*mm, 45*mm, A4[0] - 30*mm, 45*mm)
    # Footer on cover
    canvas.setFont('ArialUni', 8)
    canvas.setFillColor(LIGHT_GRAY)
    canvas.drawCentredString(A4[0]/2, 30*mm, 'Zokura Foundation 2026')
    canvas.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        topMargin=25*mm, bottomMargin=25*mm,
        leftMargin=25*mm, rightMargin=25*mm
    )

    story = []
    B = styles['body']
    H1 = styles['h1']
    H2 = styles['h2']
    Q = styles['quote']
    R = styles['ref']

    # ── COVER PAGE ──
    story.append(Spacer(1, 60*mm))
    story.append(Paragraph('Sijoittaminen', styles['title']))
    story.append(Paragraph('ammattina ja tieteenalana', styles['subtitle']))
    story.append(Spacer(1, 8*mm))
    story.append(HRFlowable(width='40%', thickness=1, color=GOLD, spaceAfter=8*mm))
    story.append(Paragraph('Historian kaaret, teorian perustukset ja tulevaisuuden horisontit', styles['subtitle']))
    story.append(Spacer(1, 20*mm))
    story.append(Paragraph('Kodo Zokura', styles['author']))
    story.append(Paragraph('Maaliskuu 2026', styles['author']))
    story.append(PageBreak())

    # ── SISALLYSLUETTELO ──
    story.append(Spacer(1, 10*mm))
    story.append(Paragraph('Sisallysluettelo', H1))
    story.append(Spacer(1, 4*mm))

    toc_items = [
        ('1.', 'Sijoittaminen ammattina \u2014 historia ja nykypaiva'),
        ('2.', 'Sijoittaminen tieteenalana'),
        ('3.', 'Keskeiset teoriat'),
        ('4.', 'Tulevaisuus: uudet paradigmat'),
        ('5.', 'Johtopaatos: mihin sijoittaminen on menossa?'),
        ('', 'Lahteet'),
    ]
    for num, title in toc_items:
        story.append(Paragraph(f'<b>{num}</b>  {title}', B))

    story.append(PageBreak())

    # ══════════════════════════════════════════
    # 1. SIJOITTAMINEN AMMATTINA
    # ══════════════════════════════════════════
    story.append(Paragraph('1. Sijoittaminen ammattina \u2014 historia ja nykypaiva', H1))

    story.append(Paragraph('1.1 Juuret: kauppiasta kvantiksi', H2))

    story.append(Paragraph(
        'Sijoittaminen ammattina on lahes yhta vanha kuin raha itse. Jo antiikin Roomassa publicani-yhtiot '
        'kerasivat paomaa ja sijoittivat valtionurakoihin \u2014 eraanlaisia proto-rahastoja, joissa '
        'riski jaettiin ja tuotto toivottiin. Keskiajan Italiassa Medicit ja muut pankkiirisuvut '
        'ammattimaistivat paoman allokoinnin taiteeksi, jonka sivutuotteena syntyi renessanssi. '
        'Ei hassumpi ROI.', B))

    story.append(Paragraph(
        'Amsterdamin porssiin perustaminen vuonna 1602 Alankomaiden Ita-Intian kauppakomppanian '
        'osakkeille merkitsi kaannekohtaa: sijoittamisesta tuli julkinen, saannelty ja \u2014 mikae '
        'tahkeinta \u2014 likviditeettia tarjoava toimiala. Ensimmaiset porssimeklarit olivat '
        'yhdistelma kauppiasta, pelaajaa ja informaatioarbitraasin harjoittajaa.', B))

    story.append(Paragraph('1.2 Moderni ammattikuva', H2))

    story.append(Paragraph(
        'Nykyaan sijoittamisen ammattikentta on laaja spektri: salkunhoitajat, analyytikot, '
        'kvantitatiiviset tutkijat, riskienhallintaspesialistit, private equity -ammattilaiset '
        'ja venture capital -sijoittajat muodostavat ekosysteemin, joka hallinnoi globaalisti '
        'yli 100 biljoonaa dollaria (ICI, 2024). CFA-instituutin tutkinto on alan de facto -standardi, '
        'ja sen lapi paaseminen vaatii keskimaarin yli 1 000 tuntia opiskelua \u2014 laaketieteellista '
        'lahes.', B))

    story.append(Paragraph(
        'Hedge-rahastojen kultakausi 1990\u20132010-luvuilla loi kuvan sijoittajasta '
        'superhirvioen kaltaisena hahmona: George Sorosin Englannin punnan shorttaus vuonna 1992 '
        'tuotti paivaessa yli miljardin dollarin ja samalla osoitti, etta yksittainen sijoittaja '
        'voi liikuttaa kokonaisia valuuttamarkkinoita. Renessance Technologiesin Medallion-rahasto '
        'puolestaan todisti, etta matematiikka voi voittaa markkinat \u2014 keskimaarainen vuosituotto '
        '66 % ennen kuluja vuosina 1988\u20132018 (Zuckerman, 2019).', B))

    story.append(Paragraph(
        '<i>\u201CPahin asia sijoittamisessa on oikein oleminen vaarasta syysta. '
        'Se opettaa sinulle kaikki vaarat tavat.\u201D</i>', Q))

    # ══════════════════════════════════════════
    # 2. SIJOITTAMINEN TIETEENALANA
    # ══════════════════════════════════════════
    story.append(Paragraph('2. Sijoittaminen tieteenalana', H1))

    story.append(Paragraph('2.1 Rahoitusteoria: tieteen askeleet', H2))

    story.append(Paragraph(
        'Rahoitusteoria tieteenalana on suhteellisen nuori. Louis Bachelierin vaitoskirja '
        '<i>Theorie de la speculation</i> (1900) oli ensimmainen yritys mallintaa osakkeiden '
        'hintaliikkeita matemaattisesti \u2014 viisikymmentae vuotta ennen kuin kukaan muu '
        'alkoi ottaa ajatusta tosissaan. Bachelier paatyi siihen, etta hinnat seuraavat '
        'satunnaiskulkua (random walk), mika on yhae rahoitusteorian peruspilareita.', B))

    story.append(Paragraph(
        'Tieteenalana rahoitus yhdistaa matematiikkaa, tilastotiedetta, taloustiedetta, '
        'psykologiaa ja viime vuosina yha enamman tietojenkasittelytiedetta. Se ei ole '
        'monoliittinen kokonaisuus vaan pikemminkin kolmen paradigman vuoropuhelu: '
        'neoklassinen rahoitusteoria, kayttaytymisperusteinen rahoitus (behavioral finance) '
        'ja kvantitatiivinen rahoitus.', B))

    story.append(Paragraph('2.2 Behavioral finance: ihminen ei ole rationaalinen', H2))

    story.append(Paragraph(
        'Daniel Kahnemanin ja Amos Tverskyn prospektiteoria (1979) muutti pelin saannot. '
        'He osoittivat, etta ihmiset eivat tee paatoksia odotetun hyodyn maksimoinnin perusteella, '
        'vaan suhteessa referenssipisteeseen \u2014 ja etta tappion tuska on noin kaksi kertaa '
        'suurempi kuin vastaavan voiton ilo. Tama selittaa, miksi sijoittajat pitavat tappiollisia '
        'positioita liian pitkaaan ja myyvat voitolliset liian aikaisin (disposition effect).', B))

    story.append(Paragraph(
        'Robert Shillerin (2000) <i>Irrational Exuberance</i> toi behavioristisen nakemyksen '
        'laajemman yleison tietoisuuteen juuri IT-kuplan huipulla \u2014 ajoitus, joka itsessaan '
        'oli eraanlainen markkinatehokkuuden vastanayte. Shiller, Fama ja Hansen jakoivat '
        'taloustieteen Nobel-palkinnon vuonna 2013, mika oli akateemisen maailman tapa '
        'sanoa: \u201Cmolemmat osapuolet ovat oikeassa, mutta eri tavalla.\u201D', B))

    story.append(Paragraph('2.3 Kvantitatiivinen rahoitus', H2))

    story.append(Paragraph(
        'Kvantitatiivinen rahoitus syntyi fyysikkojen ja matemaatikkojen siirtymisesta '
        'Wall Streetille kylman sodan jaalkeen. \u201CRocket scientists\u201D alkoivat soveltaa '
        'stokastisia differentiaaliyhtaloita rahoitussovellusten hinnoitteluun, ja tuloksena '
        'oli johdannaisten hinnoittelumallien vallankumous. Tanaan kvanttirahoitus kattaa '
        'kaiken algoritmisesta kaupankaynnista riskimallinnukseen, ja se on kaeytaennoessa '
        'suurin muutosvoima markkinoiden rakenteessa.', B))

    # ══════════════════════════════════════════
    # 3. KESKEISET TEORIAT
    # ══════════════════════════════════════════
    story.append(Paragraph('3. Keskeiset teoriat', H1))

    story.append(Paragraph('3.1 Efficient Market Hypothesis \u2014 Eugene Fama (1970)', H2))

    story.append(Paragraph(
        'Faman tehokkaiden markkinoiden hypoteesi (EMH) on rahoitusteorian kiistanalaisin '
        'ja samalla vaikutusvaltaisin yksittainen idea. Sen kolme muotoa \u2014 heikko, '
        'keskivahva ja vahva \u2014 esittavat, etta markkinahinnat heijastavat saatavilla '
        'olevaa informaatiota eri asteisesti. Vahvan muodon mukaan edes sisapiiritieto '
        'ei tarjoa etua, mika on empiiristi selvaasti vaarin mutta teoreettisesti '
        'stimuloiva.', B))

    story.append(Paragraph(
        'EMH:n kaytannoellinen seuraus on indeksisijoittamisen nousu: jos markkinoita ei voi '
        'systemaattisesti voittaa, miksi yrittaa? Jack Boglen perustama Vanguard rakensi '
        'taman filosofian paaelle imperiumin, ja tanaan passiiviset rahastot hallitsevat '
        'yli puolta Yhdysvaltain osakemarkkinoiden varallisuudesta (Morningstar, 2024).', B))

    story.append(Paragraph('3.2 Modern Portfolio Theory \u2014 Harry Markowitz (1952)', H2))

    story.append(Paragraph(
        'Markowitzin portfolioteoria on yksi harvoista rahoitusteorian tuloksista, joka on '
        'seka matemaattisesti elegantti etta kaytannoellisesti hyodyllinen. Perusidea on '
        'yksinkertainen: hajauttamalla sijoituksia eri omaisuusluokkiin voidaan parantaa '
        'tuotto-riskisuhdetta. Tehokas rintama (efficient frontier) kuvaa optimaalisia '
        'portfolioita, joissa tuotto on maksimoitu annetulla riskitasolla.', B))

    story.append(Paragraph(
        'Markowitzin tyon rakensivat eteenpaein William Sharpe (Capital Asset Pricing Model, '
        '1964), joka yksinkertaisti portfolioteorian yhden muuttujan \u2014 betan \u2014 '
        'malliksi, ja myohemmin Fama ja French (1993) kolmen faktorin mallillaan. '
        'Faktorisijoittaminen on nyt oma teollisuudenhaaransa: \u201Csmart beta\u201D '
        '-rahastot hallinnoivat yli 1,5 biljoonaa dollaria.', B))

    story.append(Paragraph('3.3 Black\u2013Scholes -malli (1973)', H2))

    story.append(Paragraph(
        'Fischer Blackin ja Myron Scholesin optiohinnoittelumalli oli rahoitusteorian '
        '\u201Cnewtoninen hetki\u201D. Se osoitti, etta option hinta voidaan johtaa '
        'matemaattisesti viidestae muuttujasta: kohde-etuuden hinta, toteutushinta, '
        'juoksuaika, riskiton korko ja volatiliteetti. Mallin eleganttius on siina, '
        'etta se ei vaadi odotetun tuoton estimointia \u2014 riskineutraali hinnoittelu '
        'ohittaa koko ongelman.', B))

    story.append(Paragraph(
        'LTCM:n romahdus vuonna 1998 osoitti kuitenkin, etta malli on tyokalu, '
        'ei totuus. Merton ja Scholes \u2014 molemmat Nobel-voittajia \u2014 olivat '
        'LTCM:n neuvonantajia. Markkinat muistuttivat, etta \u201Ckartta ei ole maasto\u201D, '
        'erityisesti kun vivutus on 25:1.', B))

    story.append(Paragraph('3.4 Behavioral Finance \u2014 Kahneman &amp; Tversky', H2))

    story.append(Paragraph(
        'Prospektiteorian (1979) lisaksi kayttaytymisrahoitus on tuottanut laajan '
        'kokoelman dokumentoituja harhoja: ankkurointi, saatavuusharha, '
        'liiallinen itseluottamus, laumakaeyttaeytyminen ja mentaalinen kirjanpito. '
        'Jokainen naista on empiirisesti vahvistettu seka laboratoriossa etta '
        'todellisilla markkinoilla.', B))

    story.append(Paragraph(
        'Richard Thalerin nudge-teoria (2008) vei kayttaytymistieteen kaytannon '
        'politiikkaan: automaattinen elaekesaeastaeminen on yksi tehokkaimmista '
        'tavoista lisata saastamista, koska se hyodyntaa ihmisen taipumusta '
        'pysya oletusasetuksessa (status quo bias). Thaler sai Nobelin 2017.', B))

    # ══════════════════════════════════════════
    # 4. TULEVAISUUS
    # ══════════════════════════════════════════
    story.append(Paragraph('4. Tulevaisuus: uudet paradigmat', H1))

    story.append(Paragraph('4.1 Tekoaely ja algoritminen kaupankaeynti', H2))

    story.append(Paragraph(
        'Koneoppiminen on jo nyt markkinoiden suurin yksittaeinen kauppias: algoritmit '
        'vastaavat arviolta 60\u201375 % Yhdysvaltain osakekaupankaeynnin volyymista '
        '(JPMorgan, 2023). Syvaeoppimismallit (deep learning) pystyvat loytaemaeaen '
        'epaelineaarisia kuvioita datasta, jota ihminen ei naekisi, mutta ne kaersivaeaet '
        'myoes ylisovittamisesta (overfitting) ja selitettaevyyden puutteesta.', B))

    story.append(Paragraph(
        'Suurten kielimallien (LLM) tulo rahoitukseen avaa uusia mahdollisuuksia: '
        'sentimenttianalyysi, raporttien automaattinen tulkinta ja jopa sijoitusstrategioiden '
        'generointi luonnollisella kielella. Samalla ne tuovat uusia riskejae \u2014 '
        'kun kaikki kayttaevaeaet samoja malleja, korrelaatio nousee ja flash crash '
        '-riski kasvaa. Ironia on taeydellinen: tekoaely, joka on suunniteltu '
        'loytaemaeaen tehottomauksia, saattaa itse luoda uusia.', B))

    story.append(Paragraph('4.2 ESG ja vastuullinen sijoittaminen', H2))

    story.append(Paragraph(
        'ESG-sijoittaminen (Environmental, Social, Governance) on kasvanut '
        'niche-ilmioestae valtavirraksi: globaalit ESG-rahastot hallinnoivat yli '
        '30 biljoonaa dollaria (GSIA, 2023). Kriitikot huomauttavat, etta '
        'ESG-luokitukset korreloivat heikosti keskenaeaen \u2014 sama yhtio voi saada '
        'AAA-luokituksen yhdeltae arvioijalta ja keskinkertaisen toiselta '
        '(Berg, Kolbel &amp; Rigobon, 2022).', B))

    story.append(Paragraph(
        'Ilmastonmuutoksen taloudelliset vaikutukset ovat kuitenkin kiistattomia, '
        'ja Nordhaus\u2019n (2018) Nobel-tyoe ilmastonmuutoksen taloustieteesta '
        'on tuonut hinnoittelukysymykset keskustieteen ytimeen. Hiilineutraaliuteen '
        'siirtyminen vaatii arvioiden mukaan 3\u20135 biljoonaa dollaria vuosittaisia '
        'investointeja \u2014 sijoittamisen rooli ei ole koskaan ollut naein suuri.', B))

    story.append(Paragraph('4.3 Kryptovaluutat ja hajautettu rahoitus', H2))

    story.append(Paragraph(
        'Bitcoin syntyi vuonna 2009 vastauksena finanssikriisiin ja luottamuspulaan '
        'keskuspankkeja kohtaan. DeFi (Decentralized Finance) on vienyt ajatuksen '
        'pidemmalle: aelysopimusten avulla rakennetut rahoituspalvelut ilman '
        'vaelikaesia. Kokonaismarkkina-arvo on heilahdellut rajusti, mutta '
        'instituutionaalinen hyvaeksyntae \u2014 Bitcoin-ETF:ien hyvaeksyminen '
        'Yhdysvalloissa 2024 \u2014 on merkittaevae kaaeaennekohta.', B))

    story.append(Paragraph(
        'Lohkoketjuteknologian todellinen vaikutus saattaa lopulta olla '
        'infrastruktuurissa, ei spekulaatiossa: tokenisoidut reaaliomaisuudet, '
        'reaaliaikaiset selvitykset ja ohjelmoitava raha voivat muuttaa '
        'rahoitusmarkkinoiden perusarkkitehtuurin. Tai sitten eivaeaet. '
        'Ennustaminen on vaikeaa, erityisesti tulevaisuudesta.', B))

    story.append(Paragraph('4.4 Sijoittamisen demokratisoituminen', H2))

    story.append(Paragraph(
        'Nollakomissio-vaeaelitys (Robinhood, 2015\u2013), murto-osaomistaminen ja '
        'sosiaalisen median sijoitusyhteisoeaet (WallStreetBets, 2021) ovat muuttaneet '
        'sijoittamisen demografiaa peruuttamattomasti. GameStop-episodi tammikuussa 2021 '
        'osoitti, ettae koordinoitu vaehittaeissijoittaminen voi haastaa institutionaalisen '
        'rahavallan \u2014 ainakin hetken.', B))

    story.append(Paragraph(
        'Demokratisoituminen tuo mukanaan myoes riskejae: Dunning\u2013Kruger-efekti '
        'yhdistettynae vipuun ja FOMO:on on kallis yhdistelmae. Rahoituslukutaidon '
        'edistaeaeminen on ehkae taeaerkein yksittaeinen haaste, jonka edessae '
        'sijoitustoimiala nyt seisoo.', B))

    # ══════════════════════════════════════════
    # 5. JOHTOPAATOS
    # ══════════════════════════════════════════
    story.append(Paragraph('5. Johtopaatos: mihin sijoittaminen on menossa?', H1))

    story.append(Paragraph(
        'Sijoittaminen ammattina ja tieteenalana on kaeynyaet laaepi haemmaestyttaevaen '
        'kehityskaaren: kauppiaan intuitiosta matemaattisiin malleihin, rationaalisesta '
        'ihmiskuvasta kayttaytymisharhojen tunnistamiseen, ja ihmisen tekemaestae '
        'paeaetoeksenteosta algoritmiseen. Jokainen vaihe on lisaennyt ymmaerrystaemme '
        'mutta myoes monimutkaisuutta.', B))

    story.append(Paragraph(
        'Tulevaisuuden sijoittamisen kenttaeae muovaavat neljae voimaa: <b>tekoaely</b>, '
        'joka muuttaa informaation kaeaesittelyn ja paeaetoeksenteon; <b>kestaevyys</b>, '
        'joka pakottaa hinnoittelemaan aiemmin ulkoistetut kustannukset; '
        '<b>hajautus</b>, seka teknologinen (DeFi) ettae sosiaalinen (demokratisoituminen); '
        'ja <b>saeaentely</b>, joka yrittaeae pysyae innovaation peraeaessae.', B))

    story.append(Paragraph(
        'Yksi asia ei muutu: markkinat ovat pohjimmiltaan ihmisten (ja nyt myoes '
        'koneiden) odotuksista, peloista ja toiveista koostuva jaeaerjestelmae. '
        'Niin kauan kuin epaevarmuus on olemassa, sijoittamiselle on ammatti. '
        'Ja niin kauan kuin ihmiset ovat epaerationaalisia, tieteelle on tyoetae.', B))

    story.append(Paragraph(
        '<i>Tai kuten eras viisas kerran sanoi: \u201CMarkkinat voivat pysyae '
        'irrationaalisina pidempaeaen kuin sinae pysyt maksukykyisenae.\u201D '
        'Keynes tiesi mistae puhui \u2014 haen meni melkein itse konkurssiin '
        'ennen kuin oppi.</i>', Q))

    # ══════════════════════════════════════════
    # LAHTEET
    # ══════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph('Lahteet', H1))
    story.append(Spacer(1, 4*mm))

    refs = [
        'Bachelier, L. (1900). <i>Theorie de la speculation</i>. Annales scientifiques de l\'Ecole Normale Superieure, 17, 21\u201386.',
        'Berg, F., Kolbel, J. F. &amp; Rigobon, R. (2022). Aggregate Confusion: The Divergence of ESG Ratings. <i>Review of Finance</i>, 26(6), 1315\u20131344.',
        'Black, F. &amp; Scholes, M. (1973). The Pricing of Options and Corporate Liabilities. <i>Journal of Political Economy</i>, 81(3), 637\u2013654.',
        'Fama, E. F. (1970). Efficient Capital Markets: A Review of Theory and Empirical Work. <i>Journal of Finance</i>, 25(2), 383\u2013417.',
        'Fama, E. F. &amp; French, K. R. (1993). Common Risk Factors in the Returns on Stocks and Bonds. <i>Journal of Financial Economics</i>, 33(1), 3\u201356.',
        'GSIA (2023). <i>Global Sustainable Investment Review 2022</i>. Global Sustainable Investment Alliance.',
        'ICI (2024). <i>Investment Company Fact Book 2024</i>. Investment Company Institute.',
        'JPMorgan (2023). <i>Global Quantitative &amp; Derivatives Strategy</i>. J.P. Morgan Markets.',
        'Kahneman, D. &amp; Tversky, A. (1979). Prospect Theory: An Analysis of Decision under Risk. <i>Econometrica</i>, 47(2), 263\u2013291.',
        'Markowitz, H. (1952). Portfolio Selection. <i>Journal of Finance</i>, 7(1), 77\u201391.',
        'Morningstar (2024). <i>U.S. Fund Flows Report Q4 2023</i>. Morningstar Research.',
        'Nordhaus, W. D. (2018). Projections and Uncertainties about Climate Change in an Era of Minimal Climate Policies. <i>American Economic Journal: Economic Policy</i>, 10(3), 333\u2013360.',
        'Sharpe, W. F. (1964). Capital Asset Prices: A Theory of Market Equilibrium under Conditions of Risk. <i>Journal of Finance</i>, 19(3), 425\u2013442.',
        'Shiller, R. J. (2000). <i>Irrational Exuberance</i>. Princeton University Press.',
        'Thaler, R. H. &amp; Sunstein, C. R. (2008). <i>Nudge: Improving Decisions about Health, Wealth, and Happiness</i>. Yale University Press.',
        'Zuckerman, G. (2019). <i>The Man Who Solved the Market: How Jim Simons Launched the Quant Revolution</i>. Portfolio/Penguin.',
    ]
    for r in refs:
        story.append(Paragraph(r, R))

    # Build
    doc.build(story, onFirstPage=cover_page, onLaterPages=footer)
    print(f'PDF generated: {OUTPUT}')


if __name__ == '__main__':
    build_pdf()
