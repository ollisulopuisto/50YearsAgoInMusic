# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to Calendar Versioning (CalVer) `vYY.MM.DD.N` where N is the total commit count.

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
