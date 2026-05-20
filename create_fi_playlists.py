import sys

import spotipy
import spotipy.util as util

import config


def create_playlists():
    # We want to create playlists for the active Finnish intervals: 15, 20, 25, 30
    fi_intervals = ["15", "20", "25", "30"]
    scope = "playlist-modify-public"

    print(f"Authenticating with Spotify for user: {config.SPOTIFY_USER}...")
    token = util.prompt_for_user_token(config.SPOTIFY_USER, scope)

    if not token:
        print("Error: Could not authenticate with Spotify.")
        sys.exit(1)

    sp = spotipy.Spotify(auth=token)
    user_id = config.SPOTIFY_USER

    # Retrieve existing playlists to avoid duplicates
    print("Fetching existing playlists to check for duplicates...")
    existing_playlists = []
    limit = 50
    offset = 0
    while True:
        results = sp.current_user_playlists(limit=limit, offset=offset)
        items = results.get("items", [])
        existing_playlists.extend(items)
        if len(items) < limit:
            break
        offset += limit

    playlist_map = {p["name"].strip(): p for p in existing_playlists}

    results_dict = {}

    for interval in fi_intervals:
        title = config.get_text("playlist_title_pattern", years=interval)
        print(f"\nChecking playlist for {interval} years ago: '{title}'")

        playlist_uri = ""
        playlist_url = ""

        if title in playlist_map:
            playlist = playlist_map[title]
            playlist_uri = playlist["uri"]
            playlist_url = playlist["external_urls"]["spotify"]
            print(f"  Existing playlist found: {playlist_uri}")
        else:
            print(f"  Playlist not found. Creating public playlist: '{title}'...")
            try:
                description = f"Suomen suosituimmat singlet {interval} vuotta sitten."
                playlist = sp.user_playlist_create(
                    user=user_id, name=title, public=True, description=description
                )
                playlist_uri = playlist["uri"]
                playlist_url = playlist["external_urls"]["spotify"]
                print(f"  Successfully created: {playlist_uri}")
            except Exception as e:
                print(f"  Error creating playlist: {e}")
                continue

        results_dict[interval] = {"fi_uri": playlist_uri, "fi_url": playlist_url}

    print("\n" + "=" * 50)
    print("PLAYLIST CONFIGURATION SNIPPET:")
    print("=" * 50)
    for interval, data in results_dict.items():
        print(f"Interval: {interval}")
        print(f'  "fi_uri": "{data["fi_uri"]}",')
        print(f'  "fi_url": "{data["fi_url"]}",')
    print("=" * 50 + "\n")


if __name__ == "__main__":
    create_playlists()
