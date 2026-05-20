import collections
import datetime
import json
import os
import pickle
import sys

import spotipy
import spotipy.util as util

import config


class Notifier:
    def __init__(self, debug=False):
        self.debug = debug

    def post(self, text):
        print(f"[Notifier] {text}")


def load_charts():
    # Attempt to load from pickle first
    charts = None

    # Try custom data path first, then fallback
    data_path = config.CHART_DATA_PATH
    if not os.path.exists(data_path) and os.path.exists(
        config.CHART_DATA_FALLBACK_PATH
    ):
        data_path = config.CHART_DATA_FALLBACK_PATH

    # If it ends with .pkl, load as pickle
    if data_path.endswith(".pkl"):
        try:
            with open(data_path, "rb") as f:
                charts = pickle.load(f, encoding="latin1")
                return charts
        except Exception as e:
            print(
                f"Failed to load pickle: {e}. Trying JSON fallback.",
                file=sys.stderr,
            )
            # Try switching path to .js / .json
            data_path = data_path.replace(".pkl", ".js")

    # Load as JSON
    if os.path.exists(data_path):
        try:
            with open(data_path, encoding="utf-8") as f:
                charts = json.load(f)
                return charts
        except Exception as e:
            print(f"Failed to load JSON data from {data_path}: {e}", file=sys.stderr)

    # Try original JSON fallback if custom not found
    if data_path != config.CHART_DATA_FALLBACK_PATH and os.path.exists(
        config.CHART_DATA_FALLBACK_PATH
    ):
        try:
            with open(config.CHART_DATA_FALLBACK_PATH, encoding="utf-8") as f:
                charts = json.load(f)
                return charts
        except Exception as e:
            print(f"Failed to load fallback JSON data: {e}", file=sys.stderr)

    raise FileNotFoundError("Could not load chart database (neither pickle nor JSON).")


def parse_date(dstring):
    return datetime.datetime.strptime(dstring, "%Y-%m-%d").date()


def show_songs(charts, song_ids):
    for i, sid in enumerate(song_ids):
        if sid and str(sid) in charts["songs"]:
            song = charts["songs"][str(sid)]
            print(i, song["title"], song["artist"])


def show_week(charts, date):
    if date in charts["charts"]:
        week = charts["charts"][date]
        show_songs(charts, week)


def prep_charts(charts):
    scharts = []
    for date_string, sids in charts["charts"].items():
        date = parse_date(date_string)
        scharts.append((date, sids))
    scharts.sort()
    charts["scharts"] = scharts


def get_best_match_for_date(charts, sdate):
    if not charts.get("scharts"):
        prep_charts(charts)
    for i, (date, sids) in enumerate(charts["scharts"][:-1]):
        ndate, _ = charts["scharts"][i + 1]
        if sdate >= date and sdate < ndate:
            return date, sids
    # Fallback to the last one if it's past or equal
    if charts["scharts"] and sdate >= charts["scharts"][-1][0]:
        return charts["scharts"][-1][0], charts["scharts"][-1][1]
    return sdate, None


def save_to_playlist(sp, charts, playlist_uri, sids):
    uris = []
    for sid in sids:
        if sid and str(sid) in charts["songs"]:
            song = charts["songs"][str(sid)]
            if "uri" in song:
                uris.append(song["uri"])

    # Spotipy replace tracks requires split into chunks of 100
    chunk_size = 100
    results = []
    for i in range(0, len(uris), chunk_size):
        chunk = uris[i : i + chunk_size]
        if i == 0:
            res = sp.user_playlist_replace_tracks(
                config.SPOTIFY_USER, playlist_uri, chunk
            )
        else:
            res = sp.user_playlist_add_tracks(config.SPOTIFY_USER, playlist_uri, chunk)
        results.append(res)
    return results


def fix_name(name):
    if name.endswith(", The"):
        return "The " + name.replace(", The", "")
    else:
        return name


def fun_facts(charts, date, sids):
    sdate = date.strftime("%Y-%m-%d")
    facts = []
    artists = collections.Counter()
    shortest = None
    longest = None
    year = str(date.year)

    def add_fact(score, txt):
        facts.append((score, txt))

    def fn(song):
        return song["title"] + " by " + fix_name(song["artist"])

    def fp(p):
        return str(p)

    def intro():
        return config.get_text("this_week_in", year=year)

    for i, sid in enumerate(sids):
        if sid and str(sid) in charts["songs"]:
            song = charts["songs"][str(sid)]
            artist = fix_name(song["artist"])
            artists[artist] += 1
            if i == 0:
                add_fact(1, intro() + config.get_text("no_1_song_was", song=fn(song)))
            if song.get("peak_week") == sdate:
                score = 6 - i / 100.0
                add_fact(
                    score,
                    intro()
                    + config.get_text("reached_peak_at", song=fn(song), peak=fp(i + 1)),
                )
            if song.get("entered") == sdate:
                score = 5 - i / 100.0
                add_fact(
                    score,
                    intro()
                    + config.get_text(
                        "entered_charts_at", song=fn(song), rank=fp(i + 1)
                    ),
                )

            wc = song.get("weeks_charted", 0)
            if shortest is None or wc < shortest.get("weeks_charted", 0):
                shortest = song
            if longest is None or wc > longest.get("weeks_charted", 0):
                longest = song

            yearly_rank = song.get("yearly_rank")
            if yearly_rank is not None and yearly_rank < 10:
                score = 2 - i / 100.0
                add_fact(
                    score,
                    intro()
                    + config.get_text(
                        "top_10_song", year=year, song=fn(song), rank=fp(i + 1)
                    ),
                )

    for a, c in artists.most_common(3):
        score = 5 + c
        if c > 2:
            add_fact(
                score + c,
                intro() + config.get_text("appears_n_times", artist=a, count=c),
            )

    if shortest and shortest.get("weeks_charted"):
        add_fact(
            5,
            config.get_text(
                "only_on_charts", song=fn(shortest), weeks=shortest["weeks_charted"]
            ),
        )
    if longest and longest.get("weeks_charted"):
        add_fact(
            2,
            config.get_text(
                "on_charts_for", song=fn(longest), weeks=longest["weeks_charted"]
            ),
        )

    facts.sort(reverse=True)
    return facts


def show_fun_facts(facts):
    for score, txt in facts:
        print(score, txt)


def send_notification(notifier, feed, txt):
    msg = txt + " " + feed["playlist_url"]
    notifier.post(msg)


def notify_fun_fact(notifier, feed, facts, which):
    if len(facts) > 0:
        idx = which % len(facts)
        _, fact_text = facts[idx]
        send_notification(notifier, feed, fact_text)


def get_target_date(today, years):
    try:
        sdate = datetime.date(today.year - years, today.month, today.day)
    except ValueError:
        # leap year w00t
        delta = int(years * 0.2425)
        sdate = today - datetime.timedelta(365 * years + delta)
    return sdate


if __name__ == "__main__":
    save = True
    sdate = None

    if len(sys.argv) < 2:
        print("Usage: python radio.py [feed_key] [--date YYYY-MM-DD]")
        sys.exit(1)

    which = sys.argv[1]
    feed_config = config.get_feed_config(which)
    if not feed_config:
        print(f"Unknown feed key: {which}")
        sys.exit(1)

    years = feed_config["years"]

    if len(sys.argv) > 2 and sys.argv[2] == "--date":
        sdate = parse_date(sys.argv[3])

    if sdate is None:
        today = datetime.datetime.now().date()
        sdate = get_target_date(today, years)

    notifier = Notifier()
    scope = "playlist-modify-public"
    token = util.prompt_for_user_token(config.SPOTIFY_USER, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        try:
            charts = load_charts()
        except Exception as e:
            print(f"Error loading charts: {e}")
            sys.exit(1)

        date, sids = get_best_match_for_date(charts, sdate)
        if sids:
            if feed_config["playlist_uri"]:
                save_to_playlist(sp, charts, feed_config["playlist_uri"], sids)
                send_notification(
                    notifier,
                    feed_config,
                    config.get_text(
                        "update_message_simple", title=feed_config["title"]
                    ),
                )
            else:
                print("No playlist URI configured, skipping Spotify update.")
                facts = fun_facts(charts, date, sids)
                if facts:
                    print("Fun facts for this week:")
                    show_fun_facts(facts)
        else:
            print(config.get_text("no_chart_found", date=sdate))
    else:
        print(config.get_text("cannot_authenticate"))
