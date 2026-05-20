import json
import os
import pickle
import re
import sys
import time

import spotipy
import spotipy.util as util

import config

db_pkl_path = "chart_details_fi.pkl"
db_js_path = "chart_details_fi.js"


def clean_term(text):
    if not text:
        return ""
    # Strip LP, Single, albumi, EP tags at the end of titles
    text = re.sub(
        r"\s*\((?:LP|single|EP|albumi|CD|lps|singles)\)\s*$",
        "",
        text,
        flags=re.IGNORECASE,
    )
    # Normalize spaces
    return re.sub(r"\s+", " ", text).strip()


def save_database(db):
    print("Saving updated databases...")
    with open(db_pkl_path, "wb") as f:
        pickle.dump(db, f, protocol=pickle.HIGHEST_PROTOCOL)
    with open(db_js_path, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    print("Databases saved successfully.")


def resolve():
    if not os.path.exists(db_pkl_path):
        print(f"Error: {db_pkl_path} does not exist. Run build_fi_database.py first.")
        sys.exit(1)

    with open(db_pkl_path, "rb") as f:
        db = pickle.load(f)

    songs = db.get("songs", {})

    # Filter songs that need resolution
    songs_to_resolve = [s for s in songs.values() if not s.get("uri")]
    print(f"Total songs in database: {len(songs)}")
    print(f"Songs remaining to resolve: {len(songs_to_resolve)}")

    if not songs_to_resolve:
        print("All songs already resolved!")
        return

    # Authenticate with Spotify
    scope = "playlist-modify-public"
    token = util.prompt_for_user_token(config.SPOTIFY_USER, scope)
    if not token:
        print("Error: Could not authenticate with Spotify.")
        sys.exit(1)

    sp = spotipy.Spotify(auth=token)

    resolved_count = 0
    not_found_count = 0

    try:
        for idx, song in enumerate(songs_to_resolve):
            artist = song["artist"]
            title = song["title"]

            clean_artist = clean_term(artist)
            clean_title = clean_term(title)

            # Tier 1: Strict search
            query = f'track:"{clean_title}" artist:"{clean_artist}"'
            try:
                results = sp.search(q=query, type="track", limit=1)
                tracks = results.get("tracks", {}).get("items", [])
            except Exception as e:
                print(f"Spotify API error for strict query '{query}': {e}")
                time.sleep(2)
                continue

            # Tier 2: Loose search fallback
            if not tracks:
                query_loose = f"{clean_title} {clean_artist}"
                try:
                    results = sp.search(q=query_loose, type="track", limit=1)
                    tracks = results.get("tracks", {}).get("items", [])
                except Exception as e:
                    print(f"Spotify API error for loose query '{query_loose}': {e}")
                    time.sleep(2)
                    continue

            if tracks:
                track = tracks[0]
                uri = track.get("uri")
                song["uri"] = uri
                # Also capture details if helpful
                resolved_count += 1
                print(
                    f"[{idx + 1}/{len(songs_to_resolve)}] Found: "
                    f"'{artist} - {title}' => {uri}"
                )
            else:
                not_found_count += 1
                # Mark as tried but not found to avoid re-searching in subsequent runs
                song["uri"] = "not_found"
                print(
                    f"[{idx + 1}/{len(songs_to_resolve)}] NOT FOUND: "
                    f"'{artist} - {title}'"
                )

            # Periodically save progress (every 50 tracks)
            if (idx + 1) % 50 == 0:
                save_database(db)

            # Throttling to prevent API rate limits
            time.sleep(0.15)

    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    finally:
        save_database(db)

    print("\nResolution session completed:")
    print(f"  * Resolved: {resolved_count}")
    print(f"  * Not Found: {not_found_count}")


if __name__ == "__main__":
    resolve()
