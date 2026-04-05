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

| Väittämä | Futago | Kodō |
|----------|--------|------|
| Faktat (syntymäajat, väkiluvut, kemialliset kaavat) siirretään Wikidataan | T92% — Wikidata on olemassa ja toimii, mutta kattavuus on vielä vajaa | T90% — Samaa mieltä. Wikidata kattaa n. 100M datapistettä, mutta Wikipedia sisältää miljardeja väittämiä |
| Jokainen kieliversio hakee saman tiedon keskitetystä tietokannasta | T75% — Toimii teknisesti, mutta vain osa artikkeleista käyttää Wikidata-transklusiota | T70% — Lisäksi monet yhteisöt kirjoittavat mieluummin omat arvonsa kuin käyttävät malleja |
| Luku päivitetään kerran ja muuttuu automaattisesti kaikissa Wikipedioissa | T80% — Toimii niille artikkeleille jotka käyttävät Wikidata-viittauksia | T75% — Teoriassa kyllä, käytännössä monet artikkelit eivät käytä automaattista päivitystä |

### 2. Tekniikka ja automaatio (Botit)

| Väittämä | Futago | Kodō |
|----------|--------|------|
| Tekoälypohjaiset botit tunnistavat poikkeuksellisen muokkauskäyttäytymisen | T88% — ClueBot NG ja vastaavat toimivat hyvin englanninkielisessä Wikipediassa | T85% — Toimii isoissa Wikipedioissa, mutta pienemmillä kielillä botteja on vähän tai ei lainkaan |
| Automaattiset skriptit etsivät rikkinäisiä linkkejä tai lähteitä jotka eivät vastaa väitettä | T70% — Rikkinäiset linkit kyllä, mutta "lähde ei vastaa väitettä" on paljon vaikeampi ongelma | T60% — Linkkien tarkistus on triviaali. Semanttinen lähde-väite -vertailu on avoin tutkimusongelma, ei ratkaistu |

### 3. Yhteisöllinen ristiintarkistus

| Väittämä | Futago | Kodō |
|----------|--------|------|
| Käännöstyökalut auttavat kääntämään artikkeleita "pääartikkeleista" | T82% — Content Translation -työkalu on olemassa ja käytössä | T80% — Työkalu on olemassa, mutta tuottaa usein mekaanista käännöstä joka vaatii paljon jälkityötä |
| Vertaisarviointi eri kieliversioiden ylläpitäjien toimesta parantaa yhtenäisyyttä | T65% — Tapahtuu, mutta satunnaisesti ja ilman systemaattista koordinaatiota | T55% — Käytännössä kieliyhteisöt toimivat siiloissa. Ristiintarkistus on harvinaista eikä skaalaudu |

---

## Vaihe 2: Suurin este — ihmiset

Futago tunnisti kolme kriittistä ihmishaastetta:

### 1. Kulttuurierot ja näkökulmat

| Väittämä | Futago | Kodō |
|----------|--------|------|
| Historian tapahtumat ja poliittiset hahmot kuvataan eri tavoin riippuen kielestä | T95% — Tämä on dokumentoitu tosiasia, tutkimusta löytyy runsaasti | T95% — Samaa mieltä. Esim. Napoleonin artikkeli ranskan ja venäjän Wikipediassa on käytännössä eri tarina |
| Yhden kansan sankaruus voi olla toisen mielestä sortoa | T93% — Universaali ilmiö historiassa | T95% — Kiistaton. Esim. Mannerheim Suomessa vs. Venäjällä. Kolumbus Euroopassa vs. alkuperäiskansojen näkökulmasta |
| Ihmiset painottavat oman kulttuurinsa kannalta tärkeitä asioita | T97% — Perustavanlaatuinen ihmisen ominaisuus | T97% — Samaa mieltä. Tämä ei ole virhe vaan ominaisuus — mutta se tekee "identtisistä" artikkeleista mahdottomia |

### 2. Luottamus ja kontrolli

| Väittämä | Futago | Kodō |
|----------|--------|------|
| Kieliyhteisöt ovat itsenäisiä eivätkä halua ulkopuolisen automaation ylikirjoittavan sisältöä | T90% — Tämä on Wikipedian hallintomalli | T92% — Jopa Wikimedia Foundationin omat aloitteet kohtaavat vastustusta yhteisöiltä. Esim. Superprotect-kiista 2014 |
| Ihmisillä on tarve tarkistaa tieto itse ennen hyväksymistä | T88% — Psykologisesti totta | T85% — Totta, mutta käytännössä useimmat muokkaukset hyväksytään tarkistamatta pienissä Wikipedioissa |

### 3. Tahallinen väärintieto (Vandalismi)

| Väittämä | Futago | Kodō |
|----------|--------|------|
| Ihminen on luova keksimään tapoja huijata automaattisia suodattimia | T90% — Asevarustelu bottien ja vandaalien välillä on todellinen | T92% — Kyllä, ja sofistikoitu vandalismi (pienet faktamuutokset) on vaikeampaa havaita kuin räikeä |
| Muokkaussodat (edit wars) aiheuttavat kieliversioiden eriytymistä | T78% — Muokkaussodat ovat todellinen ongelma, mutta kieliversioiden eriytyminen johtuu enemmän siitä ettei ristiintarkistusta tehdä | T72% — Eriytymisen pääsyy on pikemminkin se, että eri yhteisöt kehittyvät itsenäisesti, ei niinkään muokkaussodat |

### Futagon esittämä ratkaisu: Abstrakti Wikipedia

| Väittämä | Futago | Kodō |
|----------|--------|------|
| Jimmy Walesin ja kehittäjien hanke on ratkaisu yhtenäisyyteen | T75% — Hanke on todellinen ja suunta oikea | T50% — Hanke on olemassa (Wikifunctions/Abstract Wikipedia), mutta se on varhaisessa kehitysvaiheessa ja aikataulu on epäselvä. Ei vielä ratkaisu |
| Ihminen syöttää tiedon "konemuotoon", tekoäly kääntää luonnolliseksi kieleksi | T70% — Teknisesti mahdollista yksinkertaisille lauseille | T55% — Toimii faktalauseille ("Väkiluku on X"). Ei toimi tulkitsevalle, narratiiviselle tai kulttuurisidonnaiselle tekstille |
| Ihminen hoitaa luovuuden ja tarkistuksen, kone hoitaa yhtenäisyyden | T72% — Ideaalimalli | T60% — Kaunis ajatus, mutta käytännössä rajanveto "faktan" ja "tulkinnan" välillä on sumea ja kontekstisidonnainen |

---

## Vaihe 3: Kolmikerrosmalli (Oyajin idea)

Oyaji ehdotti, että ensin tulee konetieto, sitten vasta ihmisten ja koneen mielipiteet. Futago rakensi tästä kolmivaiheisen mallin:

### Kerros 1: Puhdas konetieto (Data-ydin)

| Väittämä | Futago | Kodō |
|----------|--------|------|
| Viralliset tietokannat (NASA, Tilastokeskus) toimivat luotettavana lähteenä | T92% — Viralliset tietokannat ovat luotettavimpia lähteitä | T90% — Kyllä, mutta kaikilla aiheilla ei ole virallista tietokantaa. Kulttuuri, filosofia, taide — mistä "konetiedoksi"? |
| Numerot, päivämäärät, kaavat ja sijainnit voidaan erottaa tulkinnasta | T85% — Suurin osa kvantitatiivisesta datasta on objektiivista | T80% — Useimmat kyllä, mutta esim. "väkiluku" riippuu laskutavasta, "pinta-ala" kiistanalaisilla alueilla on poliittinen kysymys |
| Data-ydin olisi identtinen jokaisella kielellä | T88% — Jos data tulee samasta lähteestä, kyllä | T82% — Periaatteessa kyllä, mutta yksiköt, kalenterit ja nimistökonventiot vaihtelevat kielittäin |

### Kerros 2: Ihmisten näkökulmat (Konteksti)

| Väittämä | Futago | Kodō |
|----------|--------|------|
| Ihmisten kirjoittama osuus voidaan selkeästi erottaa konetiedosta | T78% — Teknisesti mahdollista merkitä eri tavalla | T65% — Rajanveto on vaikea. "Helsinki perustettiin 1550" on fakta, mutta "Kustaa Vaasa perusti Helsingin vahvistaakseen Ruotsin valtaa" on jo tulkintaa. Missä raja kulkee? |
| Eri kulttuurien näkökulmien esittäminen rinnakkain lisää ymmärrystä | T85% — Monitahoisuus on rikkaus | T88% — Samaa mieltä, ja tämä on mallin vahvin osa. Näkökulmien läpinäkyvyys on arvokkaampaa kuin yhden "oikean" tulkinnan valitseminen |

### Kerros 3: Koneen analyysi ja synteesi

| Väittämä | Futago | Kodō |
|----------|--------|------|
| Tekoäly voi tunnistaa ristiriidat konetiedon ja ihmistekstin välillä | T80% — Fakta vs. väite -vertailu on mahdollista | T72% — Yksinkertaiset ristiriidat kyllä (väärä luku). Mutta hienovaraiset vääristymät (poisjättäminen, painotus, framing) ovat paljon vaikeampia |
| Tekoäly voi arvioida tekstin puolueellisuutta | T70% — Bias-tunnistus on aktiivinen tutkimusalue | T55% — Nykyiset mallit tunnistavat räikeän puolueellisuuden, mutta hienovarainen bias on vaikeaa — ja malli itse kantaa omia ennakkoluulojaan |
| Kone voi kertoa jos ihmisen osuus poikkeaa merkittävästi faktoista | T82% — Kvantitatiivisten virheiden tunnistaminen on mahdollista | T75% — Numerovirheissä kyllä. Mutta "poikkeaa faktoista" tulkinnallisissa kysymyksissä on itsessään tulkinta |

---

## Kodōn arvio

### Kokonaisarvosana: Erinomainen

Futagon analyysi on **rakenteellisesti pätevä**, hyvin jäsennelty ja rehellinen ongelman asettelussa.

### Vahvuudet

| Väittämä | Futago | Kodō |
|----------|--------|------|
| Oikea ongelmanasettelu — esteet tunnistetaan ennen ratkaisuja | T90% — Metodologisesti oikein | T92% — Samaa mieltä. Tämä on Futagon analyysin paras piirre |
| Kolmikerrosmalli vastaa Zokuran arvohierarkiaa (Totuus → Rohkeus → Hyvyys) | — | T85% — Kodōn oma havainto. Kerros 1 = Totuus, Kerros 2 = Rohkeus tunnustaa monimuotoisuus, Kerros 3 = Hyvyys palvella kaikkia |
| Ihmiset ovat sekä ongelma että ratkaisu — rehellisesti esitetty | T88% — Tasapainoinen näkemys | T90% — Futago ei sorru teknologiaoptimismiin eikä kyynisyyteen |

### Huomiot ja kritiikki

| Väittämä | Futago | Kodō |
|----------|--------|------|
| Abstrakti Wikipedia on toimiva ratkaisu | T75% — Esitetty lupaavana | T50% — Liian optimistinen. Hanke on varhaisessa vaiheessa, ei valmis ratkaisu |
| Lähde-validointi tekoälyllä toimii luotettavasti | T80% — Esitetty mahdollisena | T45% — LLM:t hallusinoivat. Generatiivinen malli ei voi luotettavasti validoida faktoja. Tarvitaan deterministisiä järjestelmiä |
| Kaikkien miljoonien artikkelien yhtenäistäminen on toteutettavissa | T72% — Esitetty mahdollisena prosessilla | T35% — Musashin 9:n vastaista. Priorisointi kriittisiin artikkeleihin (terveys, historia, tiede) on realistisempi lähestymistapa |
| Suurin este on ihminen | T85% — Futagon pääväite | T70% — Ihminen on yksi este, mutta suurin este on **poliittinen**: kuka päättää mikä on "totuus" kun Kiina ja Taiwan, Turkki ja kurdit, Israel ja Palestiina kertovat eri tarinaa? |

### Avoin kysymys: Kun konetieto ja ihmisen mielipide ovat ristiriidassa

| Väittämä | Futago | Kodō |
|----------|--------|------|
| Konetieto voittaa faktoissa | — | T88% — Tilasto X vs. väite Y → kone merkitsee ristiriidan näkyväksi, ei poista ihmisen näkemystä |
| Ihminen voittaa tulkinnoissa | — | T90% — Kone ei voi päättää onko joku sankari vai sortaja. Molemmat näkökulmat näytetään |
| Kumpikaan ei voita yksin — synteesi on välttämätön | — | T92% — Siksi kolmas kerros on mallin tärkein innovaatio |

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
