# 50 Year Radio — TODO

Projektin tavoite- ja edistymisseuranta.
Versiointi: CalVer `vYY.MM.DD.N` (N = kokonaiscommitmäärä).

**Nykyinen versio**: v26.05.20.10

---

## Vaihe 1: Perusinfra kuntoon ✅

- [x] Migroitu `uv`-projektinhallintaan (`pyproject.toml`)
- [x] Ruff-lintteri konfiguroitu ja kaikki virheet korjattu
- [x] Pytest-testit: 15 testiä, kaikki läpäisevät
- [x] Pytest `pythonpath` korjattu (moduulien import testeissä)
- [x] Suomenkielinen lokalisointi (`config.py` fi-stringit)
- [x] Suomalainen listatietokanta rakennettu (`chart_details_fi.js`)
- [x] CHANGELOG.md luotu (Keep a Changelog -muoto)
- [x] TODO.md luotu projektin seurantaan

---

## Vaihe 2: Dynaamiset vuosi-intervallit ✅

Suomalainen data kattaa **1988–2013**. Vuonna 2026 toimivat intervallit:

| Intervalli | Kohdevuosi | Status | Huomio |
|-----------|------------|--------|--------|
| 15 v. | 2011 | ✅ Lisätty | 52 listaa/v |
| 20 v. | 2006 | ✅ Olemassa | 52 listaa/v |
| 25 v. | 2001 | ✅ Lisätty | 53 listaa/v |
| 30 v. | 1996 | ✅ Olemassa | 53 listaa/v |

- [x] Lisää intervallit 15, 25 `config.py` → `DEFAULT_PLAYLISTS`
- [x] Toteuta `get_available_feeds(charts)` — auto-discovery, 90pv proximity check
- [x] `update_radio.py` ohittaa automaattisesti intervallit joille ei ole dataa
- [x] Testit uusille intervalleille (6 uutta testiä)
- [x] Päätös: intervallit 15–30 (5v välein) fi-lokaalilla

---

## Vaihe 3: Spotify-soittolistat (fi)

- [x] Luo Spotify-soittolistat kullekin suomalaiselle intervallille
- [x] Tallenna playlist-URI:t `config.py`:n `fi_uri`/`fi_url`-kenttiin
- [ ] Testaa manuaalisesti yksittäisen listan päivitys

---

## Vaihe 4: Viikoittainen automaattipäivitys

- [x] Päätös: GitHub Actions cron
- [x] Toteuta valittu automaatiomekanismi (GitHub Actions workflows)
- [x] `update_radio.py`: `--dry-run` ja `--check-data` -moodit
- [x] Spotify-credentialit turvallisesti (secrets/env via python-dotenv)
- [ ] Testaa viikoittainen ajo (odottaa julkaisua)

---

## Vaihe 5: Notifikaatiot ja julkaisu

- [ ] Korvaa Notifier-stub oikealla ilmoitusjärjestelmällä (esim. Slack, Mastodon, RSS)
- [x] Päivitä README.md vastaamaan nykytilaa
- [x] Poista vanhat Twitter-viittaukset

---

## Tekniset parannukset (backlog)

- [ ] Resolve-spotify-urit suomalaiselle datalle (kaikki kappaleet)
- [x] CI/CD-pipeline (GitHub Actions: lint + test jokainen push)
- [ ] Datan laadun tarkistus: paljonko kappaleista puuttuu Spotify-URI
- [ ] Harkitse: voiko dataa täydentää (2013→nykyhetki)?
- [ ] Harkitse: englanninkielisen datan päivitys (loppuu 2013-09)
