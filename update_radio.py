import datetime
import sys

import spotipy
import spotipy.util as util

import config
import radio


def update_feed(sp, charts, notifier, feed, *, dry_run=False):
    today = datetime.datetime.now().date()
    sdate = radio.get_target_date(today, feed["years"])
    date, sids = radio.get_best_match_for_date(charts, sdate)
    if sids:
        description = config.get_playlist_description(date)

        if dry_run:
            print(f"[dry-run] Would update: {feed['title']} ({date})")
            print(f"[dry-run] Description: {description}")
            return

        if feed["playlist_uri"]:
            radio.save_to_playlist(sp, charts, feed["playlist_uri"], sids)
            # Update playlist description and name with chart week metadata
            try:
                new_title = config.get_playlist_title(feed["years"], date)
                sp.playlist_change_details(
                    feed["playlist_uri"], name=new_title, description=description
                )
            except Exception as e:
                print(f"Warning: could not update description: {e}")
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


def check_data(charts):
    """Report data availability for all configured intervals."""
    today = datetime.datetime.now().date()
    max_gap = datetime.timedelta(days=90)
    print(f"Data availability check ({today}):\n")
    for _years_str, cfg in sorted(
        config.get_all_feeds().items(), key=lambda x: int(x[0])
    ):
        target = radio.get_target_date(today, cfg["years"])
        date, sids = radio.get_best_match_for_date(charts, target)
        if sids is not None and abs(date - target) <= max_gap:
            gap = abs(date - target).days
            note = f" (±{gap}d)" if gap > 7 else ""
            print(f"  ✅ {cfg['title']:40s} → {date} ({len(sids)} tracks){note}")
        else:
            print(f"  ❌ {cfg['title']:40s} → no data for {target}")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    data_check = "--check-data" in sys.argv
    # Remove flag args for feed name parsing
    feed_args = [a for a in sys.argv[1:] if a not in ("--dry-run", "--check-data")]

    notifier = radio.Notifier()

    try:
        charts = radio.load_charts()
    except Exception as e:
        print(f"Error loading charts: {e}")
        sys.exit(1)

    radio.prep_charts(charts)

    # --check-data: report and exit
    if data_check:
        check_data(charts)
        sys.exit(0)

    # For dry-run we don't need Spotify auth
    sp = None
    if not dry_run:
        scope = "playlist-modify-public"
        token = util.prompt_for_user_token(config.SPOTIFY_USER, scope)

        if not token:
            print(config.get_text("cannot_authenticate"))
            sys.exit(1)

        sp = spotipy.Spotify(auth=token)

    # Use only feeds with available data
    available = config.get_available_feeds(charts)

    if feed_args:
        for name in feed_args:
            if name in available:
                update_feed(sp, charts, notifier, available[name], dry_run=dry_run)
            elif name in config.get_all_feeds():
                print(f"No chart data available for interval: {name}")
            else:
                print(f"Unknown feed name: {name}")
    else:
        for _, feed in sorted(available.items(), key=lambda x: int(x[0])):
            update_feed(sp, charts, notifier, feed, dry_run=dry_run)
