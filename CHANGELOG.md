# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to Calendar Versioning (CalVer) `vYY.MM.DD.N` where N is the total commit count.

## [v26.05.21.16] - 2026-05-21

### Changed
- Reverted Finnish playlist descriptions to show weekly precision ("viikko X") and exact blog URLs for each chart mapped dynamically from the sidebar.

## [v26.05.21.15] - 2026-05-21

### Changed
- Appended a blog search link (https://suomenradiolistat.blogspot.com/search?q={year}) to the Finnish playlist descriptions.
- Removed mentions of the Whitburn Project from `README.md`.
- Added credit to Paul Lamere for the original source code in `README.md`.
- Updated table titles in `README.md` to use the new "Suomen soitetuimmat X vuotta sitten" naming.

## [v26.05.21.14] - 2026-05-21

### Changed
- Updated Finnish playlist titles to "Suomen soitetuimmat X vuotta sitten" to reflect the actual data from Timo Pennanen.
- Updated Finnish playlist descriptions to "Radiossa eniten soineet kappaleet [kuukausi] vuonna [vuosi]." as the data is monthly rather than weekly.

## [v26.05.20.11] - 2026-05-20

### Added
- Data sources section in README crediting Timo's blogs ([Suomen radiolistat](https://suomenradiolistat.blogspot.com/), [Listablogi](https://listablogi.blogspot.com/)).

### Changed
- Updated `chart_details_fi.js` and `chart_details_fi.pkl` with latest Spotify URI resolutions (~1200/3500 tracks identified).

## [v26.05.20.10] - 2026-05-20

### Added
- Playlist descriptions now show the original chart week, e.g. "Suomen virallinen singlelista, viikko 20, toukokuu 2011."
- Localized month names (Finnish and English) in `config.py`.
- `get_playlist_description()` and `get_month_name()` helper functions.

## [v26.05.20.9] - 2026-05-20

### Fixed
- `save_to_playlist` now gracefully skips playlists when no songs have resolved Spotify URIs, preventing crashes in the weekly workflow.

## [v26.05.20.8] - 2026-05-20

### Changed
- Rewrote `README.md` to reflect current project state (Finnish playlists, uv, GitHub Actions, no Twitter).
- Removed legacy `get_tweet_count()` function and `--tweet` CLI mode from `radio.py`.

### Removed
- All Twitter/tweepy references from codebase and documentation.

## [v26.05.20.7] - 2026-05-20

### Added
- Configured generated Finnish Spotify playlist URIs and URLs for intervals 15, 20, 25, and 30 under `DEFAULT_PLAYLISTS` in `config.py`.

## [v26.05.20.6] - 2026-05-20

### Changed
- Updated Finnish playlist title pattern to `"Suomen top-listat {years} vuotta sitten"`.

## [v26.05.20.5] - 2026-05-20

### Added
- Year intervals 15 and 25 to `DEFAULT_PLAYLISTS` in `config.py`.
- `get_available_feeds(charts)` auto-discovery function that filters intervals by actual chart data availability (90-day proximity check).
- `--dry-run` mode in `update_radio.py` — previews updates without Spotify auth.
- `--check-data` mode in `update_radio.py` — reports data availability for all intervals.
- 6 new tests: interval config, auto-discovery filtering, localized titles, target date calculations.
- `python-dotenv` integration to load credentials from a local `.env` file automatically.
- `.env.example` template for configuration settings.
- GitHub Actions CI workflow (`ci.yml`) to run linting, formatting, and unit tests.
- GitHub Actions scheduled workflow (`update_playlists.yml`) to automatically update playlists weekly using cached credentials.

### Changed
- `update_radio.py` rewritten to use `get_available_feeds()`, automatically skipping intervals without data.
- Feeds are now sorted numerically in output.

## [v26.05.20.4] - 2026-05-20

### Fixed
- Fixed pytest `ModuleNotFoundError` by adding `pythonpath = ["."]` to pyproject.toml.
- Fixed Ruff E501 line-too-long errors in `build_fi_database.py` and `extract_blog_tables.py`.

### Added
- Created `TODO.md` for project milestone and goal tracking.

## [v26.05.20.3] - 2026-05-20

### Added
- Created `pyproject.toml` using `uv` for python workspace management.
- Configured Ruff for aggressive linting (pyflakes, pycodestyle, isort, pyupgrade, flake8-bugbear, flake8-comprehensions).
- Created `CHANGELOG.md` file.

### Changed
- Started migration of repository to Python 3.12+ and prepared Finnish localization structure.
