import datetime
import json
import pickle
import re

from bs4 import BeautifulSoup

file_path = "all_entries.json"


def clean_text(text):
    if not text:
        return ""
    text = text.replace("\xa0", " ").replace("\u200b", "")
    return re.sub(r"\s+", " ", text).strip()


def parse_week_to_monday(week_num, year_num):
    if year_num < 50:
        year = 2000 + year_num
    else:
        year = 1900 + year_num

    try:
        if week_num < 1:
            week_num = 1
        elif week_num > 53:
            week_num = 53
        d = datetime.date.fromisocalendar(year, week_num, 1)
        return d.strftime("%Y-%m-%d")
    except Exception:
        return f"{year}-06-01"


def build():
    print("Loading all_entries.json...")
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)
    entries = data["entries"]

    songs_by_key = {}  # (artist, title) -> song_dict
    charts_by_date = {}  # date_str -> list of song_ids

    song_id_counter = 100000

    print("Parsing posts and tables...")
    for entry in entries:
        content = entry.get("content", {}).get("$t", "")
        soup = BeautifulSoup(content, "html.parser")

        tables = soup.find_all("table")
        for table in tables:
            rows = table.find_all("tr")
            current_chart_date = None

            for row_idx, row in enumerate(rows):
                tds = row.find_all(["td", "th"])
                if not tds:
                    continue

                cells = [clean_text(td.get_text()) for td in tds]
                if all(c == "" for c in cells):
                    continue

                cell_str = " ".join(cells)

                # Check for chart header
                header_match = re.search(
                    r"(?:radio|control|nielsen|impact|discopress)?\s*(\d+)(?:[-–/\d]*)\s*/\s*(\d+)",  # noqa: RUF001
                    cell_str,
                    re.IGNORECASE,
                )

                is_header = False
                if header_match:
                    if any(
                        w in cell_str.upper()
                        for w in ["RADIO", "CONTROL", "NIELSEN", "IMPACT", "DISCOPRESS"]
                    ):
                        is_header = True
                    elif row_idx == 0 or len(cells) < 2:
                        is_header = True

                if is_header and header_match:
                    week_str = header_match.group(1)
                    year_str = header_match.group(2)

                    try:
                        week_num = int(week_str)
                        year_num = int(year_str)
                        current_chart_date = parse_week_to_monday(week_num, year_num)

                        if current_chart_date not in charts_by_date:
                            charts_by_date[current_chart_date] = []
                    except Exception:
                        current_chart_date = None

                elif current_chart_date and cells[0].isdigit():
                    main_rank = int(cells[0])
                    song_td = tds[-1]

                    # Split the cell text by newlines (using BeautifulSoup separator)
                    cell_lines = [
                        clean_text(line_text)
                        for line_text in song_td.get_text("\n").split("\n")
                        if clean_text(line_text)
                    ]

                    for line in cell_lines:
                        # Check if this line is a sub-entry with its
                        # own rank, e.g. "11 Fastlove"
                        sub_match = re.match(r"^(\d+)\s+(.*)", line)
                        if sub_match:
                            rank = int(sub_match.group(1))
                            song_cell = sub_match.group(2)
                        else:
                            rank = main_rank
                            song_cell = line

                        # Parse artist and title
                        if ":" in song_cell:
                            artist, song_title = song_cell.split(":", 1)
                            artist = clean_text(artist)
                            song_title = clean_text(song_title)
                        elif " - " in song_cell:
                            artist, song_title = song_cell.split(" - ", 1)
                            artist = clean_text(artist)
                            song_title = clean_text(song_title)
                        else:
                            artist = "Unknown"
                            song_title = clean_text(song_cell)

                        # Avoid empty titles
                        if not song_title:
                            continue

                        # Unique key for lookup
                        key = (artist.lower(), song_title.lower())
                        if key not in songs_by_key:
                            songs_by_key[key] = {
                                "id": song_id_counter,
                                "artist": artist,
                                "title": song_title,
                                "peak_position": rank,
                                "peak_week": current_chart_date,
                                "entered": current_chart_date,
                                "weeks_charted": 0,
                                "year": int(current_chart_date.split("-")[0]),
                                "genre": "Pop/Rock",
                                "uri": "",
                            }
                            song_id_counter += 1

                        song = songs_by_key[key]

                        # Update metrics
                        song["weeks_charted"] += 1
                        if rank < song["peak_position"]:
                            song["peak_position"] = rank
                            song["peak_week"] = current_chart_date

                        # Add song ID to chart list
                        charts_by_date[current_chart_date].append(song["id"])

    # Format database
    # Sort charts chronologically
    sorted_chart_dates = sorted(charts_by_date.keys())
    charts_dict = {
        d: charts_by_date[d] for d in sorted_chart_dates if charts_by_date[d]
    }

    # Format songs mapping string ID -> song details
    songs_dict = {}
    for song in songs_by_key.values():
        songs_dict[str(song["id"])] = song

    db = {"charts": charts_dict, "songs": songs_dict}

    print(f"Total compiled charts: {len(charts_dict)}")
    print(f"Total compiled songs: {len(songs_dict)}")

    # Write JSON database
    print("Writing chart_details_fi.js...")
    with open("chart_details_fi.js", "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

    # Write pickle database
    print("Writing chart_details_fi.pkl...")
    with open("chart_details_fi.pkl", "wb") as f:
        pickle.dump(db, f, protocol=pickle.HIGHEST_PROTOCOL)

    print("All databases successfully compiled!")


if __name__ == "__main__":
    build()
