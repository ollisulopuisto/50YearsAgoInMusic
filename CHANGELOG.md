# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to Calendar Versioning (CalVer) `vYY.MM.DD.N` where N is the total commit count.

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
