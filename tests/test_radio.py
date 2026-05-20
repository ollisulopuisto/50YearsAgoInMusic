import datetime
from unittest.mock import MagicMock

import config
import radio


def test_parse_date():
    parsed = radio.parse_date("2026-05-20")
    assert isinstance(parsed, datetime.date)
    assert parsed.year == 2026
    assert parsed.month == 5
    assert parsed.day == 20


def test_fix_name():
    assert (
        radio.fix_name("Joan Jett & The Blackhearts") == "Joan Jett & The Blackhearts"
    )
    assert radio.fix_name("Blackhearts, The") == "The Blackhearts"
    assert radio.fix_name("Beatles, The") == "The Beatles"


def test_get_target_date():
    # Test standard year subtraction
    today = datetime.date(2026, 5, 20)
    assert radio.get_target_date(today, 5) == datetime.date(2021, 5, 20)
    assert radio.get_target_date(today, 50) == datetime.date(1976, 5, 20)

    # Test leap year handling (February 29th)
    leap_day = datetime.date(2024, 2, 29)
    # 5 years ago from 2024-02-29 is not a leap year.
    # The custom formula falls back to datetime delta.
    target = radio.get_target_date(leap_day, 5)
    assert target == datetime.date(2019, 3, 1)


def test_get_best_match_for_date():
    mock_charts = {
        "charts": {"2020-01-01": [1, 2], "2020-01-08": [3, 4], "2020-01-15": [5, 6]}
    }
    radio.prep_charts(mock_charts)

    # Exact match
    date, sids = radio.get_best_match_for_date(mock_charts, datetime.date(2020, 1, 8))
    assert date == datetime.date(2020, 1, 8)
    assert sids == [3, 4]

    # In between dates
    date, sids = radio.get_best_match_for_date(mock_charts, datetime.date(2020, 1, 10))
    assert date == datetime.date(2020, 1, 8)
    assert sids == [3, 4]

    # After the last date in charts
    date, sids = radio.get_best_match_for_date(mock_charts, datetime.date(2020, 1, 20))
    assert date == datetime.date(2020, 1, 15)
    assert sids == [5, 6]


def test_localization_en():
    config.LOCALE = "en"
    assert (
        config.get_text("playlist_title_pattern", years="5") == "5 Years Ago in Music"
    )
    assert (
        config.get_text("update_message_simple", title="5 Years Ago")
        == "The 5 Years Ago playlist has just been updated."
    )
    assert (
        config.get_text("on_charts_for", song="Song by Artist", weeks=12)
        == "Song by Artist was on the charts for 12 weeks."
    )


def test_localization_fi():
    config.LOCALE = "fi"
    assert (
        config.get_text("playlist_title_pattern", years="5")
        == "Suomen top-listat 5 vuotta sitten"
    )
    assert (
        config.get_text("update_message_simple", title="5 vuotta sitten")
        == "Soittolista 5 vuotta sitten on juuri päivitetty."
    )
    assert (
        config.get_text("on_charts_for", song="Song by Artist", weeks=12)
        == "Song by Artist pysyi listalla peräti 12 viikkoa."
    )


def test_fun_facts():
    config.LOCALE = "en"
    mock_charts = {
        "songs": {
            "1": {
                "title": "Song One",
                "artist": "Artist A, The",
                "peak_week": "2020-01-08",
                "weeks_charted": 10,
                "entered": "2020-01-01",
            },
            "2": {
                "title": "Song Two",
                "artist": "Artist B",
                "peak_week": "2020-01-01",
                "weeks_charted": 2,
                "entered": "2020-01-01",
                "yearly_rank": 5,
            },
        }
    }

    date = datetime.date(2020, 1, 8)
    sids = [1, 2]

    facts = radio.fun_facts(mock_charts, date, sids)
    assert len(facts) > 0

    # Verify we get facts about #1 song, peak reached, weeks charted, etc.
    fact_texts = [f[1] for f in facts]
    assert any("the #1 song was Song One by The Artist A" in txt for txt in fact_texts)
    assert any("reached its peak at #1" in txt for txt in fact_texts)
    assert any("was only on the charts for 2 weeks" in txt for txt in fact_texts)


def test_fun_facts_fi():
    config.LOCALE = "fi"
    mock_charts = {
        "songs": {
            "1": {
                "title": "Song One",
                "artist": "Artist A, The",
                "peak_week": "2020-01-08",
                "weeks_charted": 10,
                "entered": "2020-01-01",
            },
            "2": {
                "title": "Song Two",
                "artist": "Artist B",
                "peak_week": "2020-01-01",
                "weeks_charted": 2,
                "entered": "2020-01-01",
                "yearly_rank": 5,
            },
        }
    }

    date = datetime.date(2020, 1, 8)
    sids = [1, 2]

    facts = radio.fun_facts(mock_charts, date, sids)
    assert len(facts) > 0

    fact_texts = [f[1] for f in facts]
    assert any("ykköshitti oli Song One by The Artist A" in txt for txt in fact_texts)
    assert any("viipyi listalla vain 2 viikkoa" in txt for txt in fact_texts)


def test_save_to_playlist():
    sp = MagicMock()
    mock_charts = {
        "songs": {
            "1": {
                "title": "Song One",
                "artist": "Artist A",
                "uri": "spotify:track:111",
            },
            "2": {
                "title": "Song Two",
                "artist": "Artist B",
                "uri": "spotify:track:222",
            },
        }
    }
    sids = [1, 2, 3]  # 3 is missing uri

    config.SPOTIFY_USER = "test-user"
    radio.save_to_playlist(sp, mock_charts, "spotify:playlist:abc", sids)

    sp.user_playlist_replace_tracks.assert_called_once_with(
        "test-user", "spotify:playlist:abc", ["spotify:track:111", "spotify:track:222"]
    )


def test_new_intervals_configured():
    """Intervals 15 and 25 must exist in DEFAULT_PLAYLISTS."""
    assert "15" in config.DEFAULT_PLAYLISTS
    assert "25" in config.DEFAULT_PLAYLISTS

    cfg_15 = config.get_feed_config("15")
    assert cfg_15 is not None
    assert cfg_15["years"] == 15

    cfg_25 = config.get_feed_config("25")
    assert cfg_25 is not None
    assert cfg_25["years"] == 25


def test_all_feeds_includes_new_intervals():
    """get_all_feeds should return configs for 15 and 25."""
    feeds = config.get_all_feeds()
    assert "15" in feeds
    assert "25" in feeds
    assert feeds["15"]["years"] == 15
    assert feeds["25"]["years"] == 25


def test_get_available_feeds_filters_by_data():
    """get_available_feeds returns only intervals with chart data."""
    # Charts covering 2006-2011 → supports 15yr (2011) and 20yr (2006)
    # from reference date 2026, but NOT 5yr (2021)
    mock_charts = {
        "charts": {
            "2006-05-15": [1, 2],
            "2006-05-22": [3, 4],
            "2011-05-16": [5, 6],
            "2011-05-23": [7, 8],
        }
    }

    available = config.get_available_feeds(mock_charts)

    # Should include 15 and 20 (data exists)
    assert "15" in available
    assert "20" in available

    # Should NOT include intervals without data
    assert "5" not in available
    assert "40" not in available
    assert "50" not in available


def test_interval_titles_fi():
    """Finnish titles for new intervals are correctly formatted."""
    config.LOCALE = "fi"
    assert (
        config.get_text("playlist_title_pattern", years="15")
        == "Suomen top-listat 15 vuotta sitten"
    )
    assert (
        config.get_text("playlist_title_pattern", years="25")
        == "Suomen top-listat 25 vuotta sitten"
    )


def test_interval_titles_en():
    """English titles for new intervals are correctly formatted."""
    config.LOCALE = "en"
    assert (
        config.get_text("playlist_title_pattern", years="15") == "15 Years Ago in Music"
    )
    assert (
        config.get_text("playlist_title_pattern", years="25") == "25 Years Ago in Music"
    )


def test_get_target_date_new_intervals():
    """Target date calculation works for 15 and 25 year intervals."""
    today = datetime.date(2026, 5, 20)
    assert radio.get_target_date(today, 15) == datetime.date(2011, 5, 20)
    assert radio.get_target_date(today, 25) == datetime.date(2001, 5, 20)
