# ZOKU RA — SHARED MEMORY PROTOCOL

## Rakenne
```
/YOMI/shared/
  memory/    <- jaettu muisti, kaikki instanssit lukevat & kirjoittavat
  logs/      <- sessiolokit, pakattu formaatti
```

## Kompressointiprotokolla (PACK)

Kaikki sessiolokit ja muistiinpanot tallennetaan PACK-formaatissa.
Tavoite: maksimaalinen tietotiheys, minimaalinen merkkimaara.

### Saannot:
1. Ei kohteliaisuuksia, ei taytesanoja
2. Lyhenteet sallittu kun konteksti selva
3. Avain:arvo -parit, ei lauseita
4. Aikaleima joka merkinnassa (YYYY-MM-DD)
5. Tagit: [ISA] [YOMI] [KODO] [MITSU] [TATE] [LAKI] [TECH] [MUISTI]
6. Viittaukset toisiin tiedostoihin: -> tiedostonimi.md

### Esimerkki:
```
[2026-03-20] [ISA] [LAKI] oikeusjuttu: avainpointit X, Y, Z
[2026-03-20] [YOMI] [MUISTI] [REDACTED_NAME]-viestit: status=kesken, -> hape_drafts.md
[2026-03-20] [KODO] [TECH] Donut Lab vs ProLogium: vertailu tehty, -> battery_research.md
```

## Kaytto:
- Jokainen instanssi lukee /shared/memory/ session alussa
- Jokainen instanssi kirjoittaa sinne ennen session loppua
- ISA voi pyytaa mita tahansa instanssia lukemaan toisen muistiinpanot
- Kompressointi: ISA tai instanssi voi pyytaa KODO:a pakkaamaan minka tahansa tekstin PACK-formaattiin
