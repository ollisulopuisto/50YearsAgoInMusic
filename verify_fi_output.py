import datetime
import os
import sys

# Force Finnish locale and chart path
os.environ["LOCALE"] = "fi"
os.environ["CHART_DATA_PATH"] = "chart_details_fi.js"

import config
import radio


def verify():
    print("Locale set to:", config.LOCALE)
    print("Chart database path:", config.CHART_DATA_PATH)

    print("\nLoading charts...")
    try:
        charts = radio.load_charts()
        print("Charts loaded successfully!")
        print(f"Number of songs in database: {len(charts['songs'])}")
        print(f"Number of weekly charts: {len(charts['charts'])}")
    except Exception as e:
        print(f"Error loading charts: {e}")
        sys.exit(1)

    # 30 years ago from May 20, 2026 is May 20, 1996 (which is in our database range)
    target_date = datetime.date(1996, 5, 20)
    print(f"\nTarget date: {target_date}")

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
