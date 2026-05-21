import os

import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

# Set defaults
LOCALE = os.environ.get("LOCALE", "en").lower()  # 'en' or 'fi'
SPOTIFY_USER = os.environ.get("SPOTIFY_USER", "dst")

# Chart Data configuration
CHART_DATA_PATH = os.environ.get(
    "CHART_DATA_PATH", "chart_details_fi.js" if LOCALE == "fi" else "chart_details.js"
)

# Fallback path if custom not found (e.g., fallback to original js file)
CHART_DATA_FALLBACK_PATH = "chart_details.js"

# Localization strings
LOCALIZED_STRINGS = {
    "en": {
        "playlist_title_pattern": "{years} Years Ago in Music",
        "playlist_description": (
            "Top chart from week {week}, {month} {year}."
            " Updated weekly by 50 Year Radio."
        ),
        "update_message": (
            "The {title} playlist has been updated for the week of {date}. {url}"
        ),
        "update_message_simple": "The {title} playlist has just been updated.",
        "this_week_in": "This week in {year} ",
        "no_1_song_was": "the #1 song was {song}",
        "reached_peak_at": "{song} reached its peak at #{peak}",
        "entered_charts_at": "{song} entered the charts at #{rank}",
        "top_10_song": "top 10 song of {year} {song} was at #{rank}",
        "appears_n_times": "{artist} appears on the chart {count} times.",
        "only_on_charts": "{song} was only on the charts for {weeks} weeks.",
        "on_charts_for": "{song} was on the charts for {weeks} weeks.",
        "no_chart_found": "no chart found for {date}",
        "cannot_connect": "can't connect to spotify",
        "cannot_authenticate": "can't authenticate for spotify",
    },
    "fi": {
        "playlist_title_pattern": "Suomen soitetuimmat {years} vuotta sitten",
        "playlist_title_dynamic": "Suomen soitetuimmat {years} vuotta sitten "
        "({week}/{year})",
        "playlist_description": (
            "Radiossa eniten soineet kappaleet, viikko {week}, {month} {year}. "
            "Lähde: {url}"
        ),
        "update_message": "Soittolista {title} on päivitetty viikolle {date}. {url}",
        "update_message_simple": "Soittolista {title} on juuri päivitetty.",
        "this_week_in": "Tällä viikolla vuonna {year} ",
        "no_1_song_was": "ykköshitti oli {song}",
        "reached_peak_at": "{song} saavutti huippunsa sijalla #{peak}",
        "entered_charts_at": "{song} nousi listalle sijalle #{rank}",
        "top_10_song": "vuoden {year} top 10 -kappale {song} oli sijalla #{rank}",
        "appears_n_times": "{artist} esiintyy listalla {count} kertaa.",
        "only_on_charts": "{song} viipyi listalla vain {weeks} viikkoa.",
        "on_charts_for": "{song} pysyi listalla peräti {weeks} viikkoa.",
        "no_chart_found": "listaa ei löytynyt päivämäärälle {date}",
        "cannot_connect": "yhteys Spotifyyn epäonnistui",
        "cannot_authenticate": "kirjautuminen Spotifyyn epäonnistui",
    },
}

MONTH_NAMES = {
    "en": [
        "",
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ],
    "fi": [
        "",
        "tammikuu",
        "helmikuu",
        "maaliskuu",
        "huhtikuu",
        "toukokuu",
        "kesäkuu",
        "heinäkuu",
        "elokuu",
        "syyskuu",
        "lokakuu",
        "marraskuu",
        "joulukuu",
    ],
}


def get_text(key, **kwargs):
    locale = LOCALE if LOCALE in LOCALIZED_STRINGS else "en"
    text = LOCALIZED_STRINGS[locale].get(key, LOCALIZED_STRINGS["en"].get(key, ""))
    return text.format(**kwargs)


def get_month_name(month):
    """Return localized month name (1-indexed)."""
    locale = LOCALE if LOCALE in MONTH_NAMES else "en"
    return MONTH_NAMES[locale][month]


def get_blog_url(chart_date):
    """Return the exact blog URL for the chart date."""
    from blog_links import BLOG_LINKS

    year = chart_date.year
    month = chart_date.month

    if year == 1988:
        key = (1988, 1, 1)
    elif 1989 <= year <= 1997:
        part = 1 if month <= 6 else 2
        key = (year, part, 2)
    elif 1998 <= year <= 2013:
        part = (month - 1) // 3 + 1
        key = (year, part, 4)
    else:
        return f"https://suomenradiolistat.blogspot.com/search?q={year}"

    return BLOG_LINKS.get(
        key, f"https://suomenradiolistat.blogspot.com/search?q={year}"
    )


def get_playlist_title(years, chart_date):
    """Build a localized playlist title dynamically from the chart date."""
    week = chart_date.isocalendar()[1]
    year = chart_date.year
    if LOCALE == "fi":
        return get_text("playlist_title_dynamic", years=years, week=week, year=year)
    return get_text("playlist_title_pattern", years=years)


def get_playlist_description(chart_date):
    """Build a localized playlist description from the chart date."""
    week = chart_date.isocalendar()[1]
    month = get_month_name(chart_date.month)
    year = chart_date.year
    url = get_blog_url(chart_date)
    return get_text("playlist_description", week=week, month=month, year=year, url=url)


# Default feed playlists (original values from plamere)
DEFAULT_PLAYLISTS = {
    "5": {
        "en_uri": "spotify:user:plamere:playlist:7L7F0RmgNOZ5O8UJX7s4RR",
        "en_url": "https://open.spotify.com/user/plamere/playlist/7L7F0RmgNOZ5O8UJX7s4RR",
        "fi_uri": "",
        "fi_url": "",
    },
    "10": {
        "en_uri": "spotify:user:plamere:playlist:4VNzdtsvmHz31W3H6eDSEF",
        "en_url": "https://open.spotify.com/user/plamere/playlist/4VNzdtsvmHz31W3H6eDSEF",
        "fi_uri": "",
        "fi_url": "",
    },
    "15": {
        "en_uri": "",
        "en_url": "",
        "fi_uri": "spotify:playlist:54i05jCvdR9mrpOn2YPyr1",
        "fi_url": "https://open.spotify.com/playlist/54i05jCvdR9mrpOn2YPyr1",
    },
    "20": {
        "en_uri": "spotify:user:plamere:playlist:1HnmSGLvzXQejvcsgob208",
        "en_url": "https://open.spotify.com/user/plamere/playlist/1HnmSGLvzXQejvcsgob208",
        "fi_uri": "spotify:playlist:48smGZScf4kG6uMC0wdX09",
        "fi_url": "https://open.spotify.com/playlist/48smGZScf4kG6uMC0wdX09",
    },
    "25": {
        "en_uri": "",
        "en_url": "",
        "fi_uri": "spotify:playlist:40LO5PadayvxBkTE6rdqj1",
        "fi_url": "https://open.spotify.com/playlist/40LO5PadayvxBkTE6rdqj1",
    },
    "30": {
        "en_uri": "spotify:user:plamere:playlist:7tsCIT87Be5AP0eaJe1lY7",
        "en_url": "https://open.spotify.com/user/plamere/playlist/7tsCIT87Be5AP0eaJe1lY7",
        "fi_uri": "spotify:playlist:4IfVQrggAfv95jBWmXkrXA",
        "fi_url": "https://open.spotify.com/playlist/4IfVQrggAfv95jBWmXkrXA",
    },
    "40": {
        "en_uri": "spotify:user:plamere:playlist:3N26XDqRfWT1DpXFBT2MlE",
        "en_url": "https://open.spotify.com/user/plamere/playlist/3N26XDqRfWT1DpXFBT2MlE",
        "fi_uri": "",
        "fi_url": "",
    },
    "50": {
        "en_uri": "spotify:user:plamere:playlist:20MRgCn9dwNPeGhNBGAlZZ",
        "en_url": "http://open.spotify.com/user/plamere/playlist/20MRgCn9dwNPeGhNBGAlZZ",
        "fi_uri": "",
        "fi_url": "",
    },
}


def get_feed_config(years_str):
    if years_str not in DEFAULT_PLAYLISTS:
        return None

    # Check environment override
    uri_env = os.environ.get(f"PLAYLIST_{years_str}_URI")
    url_env = os.environ.get(f"PLAYLIST_{years_str}_URL")

    defaults = DEFAULT_PLAYLISTS[years_str]

    if LOCALE == "fi":
        default_uri = uri_env or defaults["fi_uri"]
        default_url = url_env or defaults["fi_url"]
        default_title = get_text("playlist_title_pattern", years=years_str)
    else:
        default_uri = uri_env or defaults["en_uri"]
        default_url = url_env or defaults["en_url"]
        default_title = get_text("playlist_title_pattern", years=years_str)

    return {
        "years": int(years_str),
        "title": default_title,
        "playlist_uri": default_uri,
        "playlist_url": default_url,
    }


def get_all_feeds():
    feeds = {}
    for years_str in DEFAULT_PLAYLISTS.keys():
        cfg = get_feed_config(years_str)
        if cfg:
            feeds[years_str] = cfg
    return feeds


def get_available_feeds(charts):
    """Return only feeds that have chart data available.

    Checks each configured interval against the loaded chart
    database and returns only those with matching data.
    """
    import datetime

    # Import here to avoid circular dependency at module level
    from radio import get_best_match_for_date, get_target_date, prep_charts

    if not charts.get("scharts"):
        prep_charts(charts)

    today = datetime.datetime.now().date()
    max_gap = datetime.timedelta(days=90)
    available = {}
    for years_str, cfg in get_all_feeds().items():
        target = get_target_date(today, cfg["years"])
        matched_date, sids = get_best_match_for_date(charts, target)
        if sids is not None and abs(matched_date - target) <= max_gap:
            available[years_str] = cfg
    return available
