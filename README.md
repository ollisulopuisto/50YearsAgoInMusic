# 50 Year Radio 🎵

Spotify-soittolistoja, jotka päivittyvät viikoittain menneisyyden hittilistoille.
Suomalainen listatietokanta (1988–2013) ja kansainvälinen data (Whitburn Project).

## Aktiiviset soittolistat (fi)

| Soittolista | Intervalli | Spotify |
|---|---|---|
| Suomen top-listat 15 vuotta sitten | 15 v. | [Avaa](https://open.spotify.com/playlist/54i05jCvdR9mrpOn2YPyr1) |
| Suomen top-listat 20 vuotta sitten | 20 v. | [Avaa](https://open.spotify.com/playlist/48smGZScf4kG6uMC0wdX09) |
| Suomen top-listat 25 vuotta sitten | 25 v. | [Avaa](https://open.spotify.com/playlist/40LO5PadayvxBkTE6rdqj1) |
| Suomen top-listat 30 vuotta sitten | 30 v. | [Avaa](https://open.spotify.com/playlist/4IfVQrggAfv95jBWmXkrXA) |

Soittolistat päivitetään automaattisesti joka maanantai klo 12:00 EET (GitHub Actions).

## Käyttö

```bash
# Asenna riippuvuudet
uv sync --all-groups

# Tarkista datan saatavuus
LOCALE=fi uv run python update_radio.py --check-data

# Kuivaharjoitus (ei kirjoita Spotifyyn)
LOCALE=fi uv run python update_radio.py --dry-run

# Päivitä kaikki soittolistat
LOCALE=fi uv run python update_radio.py

# Päivitä yksittäinen intervalli
LOCALE=fi uv run python update_radio.py 20
```

## Listatietokanta

Suomalainen data on peräisin Suomen virallisista singlelista-arkistoista ja kattaa vuodet **1988–2013**.
Kansainvälinen data perustuu [The Whitburn Project](http://waxy.org/2008/05/the_whitburn_project/) -tietokantaan.

## Datalähteet

Suomalaiset listatiedot on koottu Timo Pennasen ylläpitämistä lähteistä, mistä iso kiitos!

- [Suomen radiolistat](https://suomenradiolistat.blogspot.com/) — Suomen virallisia radiosoittolistoja
- [Listablogi](https://listablogi.blogspot.com/) — Suomen virallisia myyntilistoja ja muita listatietoja

## Automaatio

- **CI**: Ruff-lintteri + pytest jokaisella pushilla (`ci.yml`)
- **Viikoittainen päivitys**: GitHub Actions cron maanantaisin (`update_playlists.yml`)

## Ympäristömuuttujat

Luo `.env`-tiedosto (ks. `.env.example`):

```
SPOTIPY_CLIENT_ID=xxx
SPOTIPY_CLIENT_SECRET=xxx
SPOTIPY_REDIRECT_URI=https://xxx/yyy
SPOTIFY_USER=käyttäjätunnus
LOCALE=fi
```

## Riippuvuudet

- Python 3.12+
- [spotipy](https://spotipy.readthedocs.io/) — Spotify Web API
- [uv](https://docs.astral.sh/uv/) — projektinhallinta

## Versiointi

CalVer: `vYY.MM.DD.N` (N = kokonaiscommitmäärä).

## Lisenssi

MIT
