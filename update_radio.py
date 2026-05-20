import datetime
import sys

import spotipy
import spotipy.util as util

import config
import radio


def update_feed(sp, charts, notifier, feed):
    today = datetime.datetime.now().date()
    sdate = radio.get_target_date(today, feed["years"])
    date, sids = radio.get_best_match_for_date(charts, sdate)
    if sids:
        if feed["playlist_uri"]:
            radio.save_to_playlist(sp, charts, feed["playlist_uri"], sids)
        else:
            print(f"Skipping playlist update for {feed['title']} (no URI configured).")

        formatted_date = date.strftime("%Y-%m-%d")
        msg = config.get_text(
            "update_message",
            title=feed["title"],
            date=formatted_date,
            url=feed["playlist_url"],
        )
        notifier.post(msg)
    else:
        print(config.get_text("no_chart_found", date=sdate))


if __name__ == "__main__":
    notifier = radio.Notifier()
    scope = "playlist-modify-public"
    token = util.prompt_for_user_token(config.SPOTIFY_USER, scope)

    if not token:
        print(config.get_text("cannot_authenticate"))
        sys.exit(1)

    sp = spotipy.Spotify(auth=token)

    try:
        charts = radio.load_charts()
    except Exception as e:
        print(f"Error loading charts: {e}")
        sys.exit(1)

    radio.prep_charts(charts)

    # Allow passing specific feeds via CLI args, else update all
    all_feeds = config.get_all_feeds()
    if len(sys.argv) > 1:
        for name in sys.argv[1:]:
            if name in all_feeds:
                update_feed(sp, charts, notifier, all_feeds[name])
            else:
                print(f"Unknown feed name: {name}")
    else:
        for _, feed in all_feeds.items():
            update_feed(sp, charts, notifier, feed)
