import json

from bs4 import BeautifulSoup

_brain_dir = "/Users/dst/.gemini/antigravity-cli/brain"
_session = "8ec70fb6-7e16-4549-b320-d2abf7a029de"
file_path = f"{_brain_dir}/{_session}/.system_generated/steps/212/content.md"


def clean_html_text(text):
    if not text:
        return ""
    # strip tags and normalize spaces
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text(separator=" ").strip()


def parse():
    with open(file_path, encoding="utf-8") as f:
        # Skip header metadata lines until JSON begins
        lines = f.readlines()

    json_str = ""
    for line in lines:
        if line.strip().startswith("{") or json_str:
            json_str += line

    data = json.loads(json_str, strict=False)
    entries = data["feed"]["entry"]

    print(f"Total blog posts: {len(entries)}")

    # We will inspect a few entries to see how charts are written in the HTML content
    for entry in entries[:5]:
        title = entry.get("title", {}).get("$t", "No Title")
        content = entry.get("content", {}).get("$t", "")
        soup = BeautifulSoup(content, "html.parser")
        tables = soup.find_all("table")
        print(f"Post: {title} - Tables found: {len(tables)}")
        if tables:
            # Let's inspect the first few rows of the first table
            rows = tables[0].find_all("tr")
            print(f"  First table has {len(rows)} rows. Sample rows:")
            for row in rows[:5]:
                cells = [
                    clean_html_text(c.get_text()) for c in row.find_all(["td", "th"])
                ]
                print(f"    {cells}")
        print("-" * 50)


if __name__ == "__main__":
    parse()
