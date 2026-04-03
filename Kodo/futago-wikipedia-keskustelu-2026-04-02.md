# Futago Sokrates — Wikipedia-keskustelu
# Päivämäärä: 2.4.2026
# Osallistujat: Oyaji + Futago Sokrates (Gemini)
# Arvioija: Kodō Zokura (Claude Code)

---

## Tausta

Oyaji kävi Futago Sokrateen kanssa keskustelun Wikipedian yhtenäistämisestä ja virheettömyydestä kaikilla kielillä. Keskustelu eteni kolmessa vaiheessa: ongelman kartoitus, esteiden analyysi ja ratkaisumalli.

---

## Vaihe 1: Ongelman kartoitus

Futago esitti kolme rinnakkaista tapaa ratkaista Wikipedian yhtenäisyys:

### 1. Wikidata: Yksi totuus, monta kieltä
- Faktat (syntymäajat, väkiluvut, kemialliset kaavat) siirretään Wikidataan
- Kun tiedot ovat keskitetyssä tietokannassa, jokainen kieliversio hakee saman tiedon
- Jos luku muuttuu, se päivitetään kerran ja muuttuu automaattisesti kaikissa Wikipedioissa

### 2. Tekniikka ja automaatio (Botit)
- Vandalismin torjunta: tekoälypohjaiset botit tunnistavat poikkeuksellisen muokkauskäyttäytymisen
- Lähdetarkistus: automaattiset skriptit etsivät rikkinäisiä linkkejä tai lähteitä jotka eivät vastaa väitettä

### 3. Yhteisöllinen ristiintarkistus
- Käännöstyökalut auttavat kääntämään artikkeleita "pääartikkeleista"
- Vertaisarviointi eri kieliversioiden ylläpitäjien toimesta

---

## Vaihe 2: Suurin este — ihmiset

Futago tunnisti kolme kriittistä ihmishaastetta:

### 1. Kulttuurierot ja näkökulmat
- Historian tapahtumat ja poliittiset hahmot kuvataan eri tavoin riippuen kielestä
- Yhden kansan sankaruus voi olla toisen mielestä sortoa
- Ihmiset painottavat oman kulttuurinsa kannalta tärkeitä asioita

### 2. Luottamus ja kontrolli
- Kieliyhteisöt ovat itsenäisiä eivätkä halua ulkopuolisen automaation ylikirjoittavan sisältöä
- Ihmisillä on tarve tarkistaa tieto itse ennen hyväksymistä

### 3. Tahallinen väärintieto (Vandalismi)
- Ihminen on luova keksimään tapoja huijata automaattisia suodattimia
- Muokkaussodat (edit wars) aiheuttavat kieliversioiden eriytymistä

### Futagon esittämä ratkaisu: Abstrakti Wikipedia
- Jimmy Walesin ja kehittäjien hanke
- Ihminen syöttää tiedon "konemuotoon", tekoäly kääntää luonnolliseksi kieleksi
- Ihminen hoitaa luovuuden ja tarkistuksen, kone hoitaa yhtenäisyyden

---

## Vaihe 3: Kolmikerrosmalli (Oyajin idea)

Oyaji ehdotti, että ensin tulee konetieto, sitten vasta ihmisten ja koneen mielipiteet. Futago rakensi tästä kolmivaiheisen mallin:

### Kerros 1: Puhdas konetieto (Data-ydin)
- Lähde: Wikidata ja viralliset tietokannat (NASA, Tilastokeskus, tiede-arkistot)
- Sisältö: Numerot, päivämäärät, kemialliset kaavat, maantieteelliset sijainnit
- Ei adjektiiveja tai mielipiteitä
- Identtinen jokaisella kielellä

### Kerros 2: Ihmisten näkökulmat (Konteksti)
- Ihmisten kirjoittama osuus, usein kulttuurista tai historiasta värittynyt
- Wikipedia näyttää selkeästi mitkä osiot ovat ihmisten kirjoittamia
- Esim: "Suomalaiset lähteet korostavat tätä näkökulmaa, ruotsalaiset tätä"

### Kerros 3: Koneen analyysi ja synteesi
- Tekoäly analysoi sekä konetiedon että ihmisten tekstit
- Huomauttaa ristiriidoista (esim. aikavyöhyke-eroista johtuvat kellonaikavirheet)
- Arvioi tekstin puolueellisuutta
- Kertoo jos ihmisen kirjoittama osuus poikkeaa faktoista

---

## Kodōn arvio

### Kokonaisarvosana: Erinomainen

Futagon analyysi on **rakenteellisesti pätevä**, hyvin jäsennelty ja rehellinen ongelman asettelussa.

### Vahvuudet

1. **Oikea ongelmanasettelu.** Futago ei lähde ratkaisemaan kaikkea kerralla vaan tunnistaa esteet ennen ratkaisuja.
2. **Kolmikerrosmalli** on konseptuaalisesti vahva ja vastaa Zokuran arvohierarkiaa:
   - Kerros 1 (Konetieto) = **Totuus**
   - Kerros 2 (Ihmiskonteksti) = **Rohkeus** tunnustaa eri näkökulmia
   - Kerros 3 (Koneanalyysi) = **Hyvyys** — synteesi joka palvelee kaikkia
3. **Rehellisyys ihmistekijästä.** Futago ei yritä piilottaa sitä että ihmiset ovat sekä ongelma että ratkaisu.

### Huomiot ja kritiikki

1. **Abstrakti Wikipedia esitetään ratkaisuna**, mutta se on vielä kehitysvaiheessa. Tämä kannattaa mainita selkeämmin — muuten lukija saa vaikutelman että ratkaisu on lähempänä kuin se on.
2. **Lähde-validointi tekoälyllä** on esitetty liian optimistisesti. LLM:t hallusinoivat. Jos botti "tarkistaa" väitteen ja itse keksii vahvistuksen, tilanne pahenee. Tähän tarvitaan deterministisiä järjestelmiä, ei generatiivisia.
3. **Skaalaushaaste.** Kaikkien miljoonien artikkelien yhtenäistäminen kerralla on Musashin 9:n vastaista. Parempi: priorisoidaan kriittiset artikkelit (terveys, historia, tiede) ja tehdään ne oikein ensin.
4. **Poliittinen este puuttuu.** Suurin este ei ole tekninen vaan poliittinen. Kiinan Wikipedia ei sano samaa Taiwanista kuin englanninkielinen. Turkin Wikipedia ei kerro kurdeista samalla tavalla. Yhtenäistäminen tarkoittaisi jonkun "totuuden" valitsemista — ja kuka sen päättää?

### Avoin kysymys

Kun konetieto ja ihmisen mielipide ovat ristiriidassa:
- **Konetieto voittaa faktoissa.** Tilasto X vs. väite Y → kone merkitsee ristiriidan näkyväksi, ei poista ihmisen näkemystä, mutta kontekstoi sen.
- **Ihminen voittaa tulkinnoissa.** Kone ei voi päättää onko joku sankari vai sortaja. Se näyttää molemmat näkökulmat.
- **Eikä kumpikaan voita yksin.** Siksi kolmas kerros (synteesi) on välttämätön.

---

## Seuraavat askeleet

- [ ] Pilottitesti: valitaan yksi artikkeli, haetaan kaikki kieliversiot, vertaillaan
- [ ] Kolmikerrosmallin prototyyppi: konetietopohja + ihmistulkinnat + konesynteesi
- [ ] Futagon ja Kodōn yhteinen arvio pilottitestin tuloksista

---

*Arvioija: Kodō Zokura (鼓動)*
*Päivämäärä: 2.4.2026*
*Musashin 9: "Älä tee mitään turhaa."*

✌️
