import datetime

import config
import radio


def verify():
    # Set locale to Finnish
    config.LOCALE = "fi"
    print("Locale set to:", config.LOCALE)

    # Load charts database.
    # Uses chart_details.js fallback if pickle is missing or fails.
    print("Loading charts...")
    charts = radio.load_charts()
    print("Charts loaded successfully!")
    print(f"Number of songs in database: {len(charts['songs'])}")
    print(f"Number of weekly charts: {len(charts['charts'])}")

    # Let's search for a chart exactly 50 years ago from today (or close to it)
    # May 20, 2026 - 50 years is May 20, 1976
    target_date = datetime.date(1976, 5, 20)
    print(f"Target date: {target_date}")

    radio.prep_charts(charts)
    best_date, sids = radio.get_best_match_for_date(charts, target_date)
    print(f"Best matching chart date: {best_date}")

    if sids:
        print("\nTop 5 songs in chart:")
        for i, sid in enumerate(sids[:5]):
            if sid and str(sid) in charts["songs"]:
                song = charts["songs"][str(sid)]
                print(f"  {i + 1}. {song['title']} - {radio.fix_name(song['artist'])}")

        print("\nFun facts generated (in Finnish):")
        facts = radio.fun_facts(charts, best_date, sids)
        for score, fact_text in facts[:10]:
            print(f"  [{score:.2f}] {fact_text}")
    else:
        print("No chart found for target date.")


if __name__ == "__main__":
    verify()
