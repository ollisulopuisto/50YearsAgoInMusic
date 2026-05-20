# 50 Year Radio — TODO

Projektin tavoite- ja edistymisseuranta.
Versiointi: CalVer `vYY.MM.DD.N` (N = kokonaiscommitmäärä).

**Nykyinen versio**: v26.05.20.4

---

## Vaihe 1: Perusinfra kuntoon ✅

- [x] Migroitu `uv`-projektinhallintaan (`pyproject.toml`)
- [x] Ruff-lintteri konfiguroitu ja kaikki virheet korjattu
- [x] Pytest-testit: 9 testiä, kaikki läpäisevät
- [x] Pytest `pythonpath` korjattu (moduulien import testeissä)
- [x] Suomenkielinen lokalisointi (`config.py` fi-stringit)
- [x] Suomalainen listatietokanta rakennettu (`chart_details_fi.js`)
- [x] CHANGELOG.md luotu (Keep a Changelog -muoto)
- [x] TODO.md luotu projektin seurantaan

---

## Vaihe 2: Dynaamiset vuosi-intervallit

Suomalainen data kattaa **1988–2013**. Vuonna 2026 toimivat intervallit:

| Intervalli | Kohdevuosi | Status | Huomio |
|-----------|------------|--------|--------|
| 15 v. | 2011 | `[ ]` Lisättävä | 52 listaa/v |
| 20 v. | 2006 | `[ ]` Olemassa (en) | 52 listaa/v |
| 25 v. | 2001 | `[ ]` Lisättävä | 53 listaa/v |
| 30 v. | 1996 | `[ ]` Olemassa (en) | 53 listaa/v |
| 35 v. | 1991 | `[ ]` Lisättävä | 22 listaa/v, harva |

- [ ] Lisää intervallit 15, 25, 35 `config.py` → `DEFAULT_PLAYLISTS`
- [ ] Toteuta `check_data_availability()` — tarkistaa onko dataa annetulle intervallille
- [ ] `get_all_feeds()` ohittaa automaattisesti intervallit joille ei ole dataa
- [ ] Testit uusille intervalleille
- [ ] Päätös: mitkä intervallit otetaan fi-lokaalilla käyttöön?

---

## Vaihe 3: Spotify-soittolistat (fi)

- [ ] Luo Spotify-soittolistat kullekin suomalaiselle intervallille
- [ ] Tallenna playlist-URI:t `config.py`:n `fi_uri`/`fi_url`-kenttiin
- [ ] Testaa manuaalisesti yksittäisen listan päivitys

---

## Vaihe 4: Viikoittainen automaattipäivitys

- [ ] Päätös: GitHub Actions cron / paikallinen crontab / Systemd timer?
- [ ] Toteuta valittu automaatiomekanismi
- [ ] `update_radio.py`: lisää `--dry-run` ja `--check-data` -moodit
- [ ] Spotify-credentialit turvallisesti (secrets/env)
- [ ] Testaa viikoittainen ajo

---

## Vaihe 5: Notifikaatiot ja julkaisu

- [ ] Korvaa Notifier-stub oikealla ilmoitusjärjestelmällä (esim. Slack, Mastodon, RSS)
- [ ] Päivitä README.md vastaamaan nykytilaa
- [ ] Poista vanhat Twitter-viittaukset

---

## Tekniset parannukset (backlog)

- [ ] Resolve-spotify-urit suomalaiselle datalle (kaikki kappaleet)
- [ ] CI/CD-pipeline (GitHub Actions: lint + test jokainen push)
- [ ] Datan laadun tarkistus: paljonko kappaleista puuttuu Spotify-URI
- [ ] Harkitse: voiko dataa täydentää (2013→nykyhetki)?
- [ ] Harkitse: englanninkielisen datan päivitys (loppuu 2013-09)
